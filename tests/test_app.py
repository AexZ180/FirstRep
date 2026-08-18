import pytest

from app import create_app
from app.extensions import db
from app.models import ExerciseLog, Onboarding, User, WorkoutPlan, WorkoutSession


@pytest.fixture
def app():
    app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-secret",
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def register(client, email="alex@example.com", password="password123"):
    return client.post(
        "/register",
        data={"email": email, "password": password},
        follow_redirects=True,
    )


def create_plan(client, goal="muscle_gain", days=3):
    return client.post(
        "/onboarding",
        data={"goal": goal, "weight": "170", "days_per_week": str(days)},
        follow_redirects=True,
    )


def test_protected_routes_redirect_anonymous_users(client):
    for route in ("/", "/onboarding", "/workout-plan"):
        response = client.get(route)
        assert response.status_code == 302
        assert "/login" in response.headers["Location"]


def test_registration_creates_user_and_session(app, client):
    response = register(client)

    assert response.status_code == 200
    with app.app_context():
        assert User.query.filter_by(email="alex@example.com").one()
    with client.session_transaction() as session:
        assert session["user_id"] is not None


@pytest.mark.parametrize("days", [1, 5, 7])
def test_onboarding_rejects_unsupported_training_frequency(app, client, days):
    register(client)
    response = client.post(
        "/onboarding",
        data={"goal": "general_fitness", "weight": "170", "days_per_week": days},
    )

    assert response.status_code == 200
    assert b"between 2 and 4" in response.data
    with app.app_context():
        assert Onboarding.query.count() == 0


def test_onboarding_creates_personalized_plan(app, client):
    register(client)
    response = client.post(
        "/onboarding",
        data={"goal": "muscle_gain", "weight": "170", "days_per_week": "3"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"3-Day Muscle Gain Plan" in response.data
    with app.app_context():
        assert Onboarding.query.count() == 1
        assert WorkoutPlan.query.count() == 1


def test_logout_requires_post_and_clears_session(client):
    register(client)

    assert client.get("/logout").status_code == 405
    response = client.post("/logout")

    assert response.status_code == 302
    with client.session_transaction() as session:
        assert "user_id" not in session


def test_workout_session_stores_set_level_performance(app):
    with app.app_context():
        user = User(email="lifter@example.com", password_hash="hashed-password")
        db.session.add(user)
        db.session.flush()

        onboarding = Onboarding(
            goal="muscle_gain",
            weight=170,
            days_per_week=3,
            user_id=user.id,
        )
        db.session.add(onboarding)
        db.session.flush()

        plan = WorkoutPlan(onboarding_id=onboarding.id, plan_json="{}")
        db.session.add(plan)
        db.session.flush()

        workout = WorkoutSession(
            user_id=user.id,
            workout_plan_id=plan.id,
            day_index=0,
        )
        workout.exercise_logs.extend(
            [
                ExerciseLog(
                    exercise_key="bench_press",
                    set_number=1,
                    reps=8,
                    weight=95,
                ),
                ExerciseLog(
                    exercise_key="bench_press",
                    set_number=2,
                    reps=7,
                    weight=95,
                ),
            ]
        )
        db.session.add(workout)
        db.session.commit()

        saved_workout = WorkoutSession.query.one()
        assert saved_workout.user.email == "lifter@example.com"
        assert saved_workout.workout_plan_id == plan.id
        assert len(saved_workout.exercise_logs) == 2
        assert saved_workout.exercise_logs[1].reps == 7


def test_user_can_start_a_day_from_their_plan(app, client):
    register(client)
    create_plan(client)

    with app.app_context():
        plan_id = WorkoutPlan.query.one().id

    response = client.post(f"/workouts/start/{plan_id}/0")

    assert response.status_code == 302
    assert "/workouts/" in response.headers["Location"]
    with app.app_context():
        workout = WorkoutSession.query.one()
        assert workout.day_index == 0
        assert workout.workout_plan_id == plan_id


def test_user_cannot_start_another_users_plan(app, client):
    register(client, email="owner@example.com")
    create_plan(client)

    with app.app_context():
        plan_id = WorkoutPlan.query.one().id

    client.post("/logout")
    register(client, email="intruder@example.com")

    response = client.post(f"/workouts/start/{plan_id}/0")

    assert response.status_code == 404
    with app.app_context():
        assert WorkoutSession.query.count() == 0


def test_start_workout_rejects_day_outside_plan(app, client):
    register(client)
    create_plan(client)

    with app.app_context():
        plan_id = WorkoutPlan.query.one().id

    response = client.post(f"/workouts/start/{plan_id}/99")

    assert response.status_code == 404
    with app.app_context():
        assert WorkoutSession.query.count() == 0


def test_completing_workout_saves_logs_and_completion_time(app, client):
    register(client)
    create_plan(client)
    with app.app_context():
        plan_id = WorkoutPlan.query.one().id

    client.post(f"/workouts/start/{plan_id}/0")
    with app.app_context():
        workout_id = WorkoutSession.query.one().id

    response = client.post(
        f"/workouts/{workout_id}/complete",
        data={
            "reps_0_1": "8",
            "weight_0_1": "95.5",
            "reps_0_2": "7",
            "weight_0_2": "95.5",
        },
    )

    assert response.status_code == 302
    with app.app_context():
        workout = db.session.get(WorkoutSession, workout_id)
        assert workout.completed_at is not None
        assert len(workout.exercise_logs) == 2
        assert workout.exercise_logs[0].exercise_key == "bench_press"
        assert workout.exercise_logs[0].weight == 95.5

    detail_response = client.get(f"/workouts/{workout_id}")
    assert detail_response.status_code == 200
    assert b'value="8"' in detail_response.data
    assert b'value="95.5"' in detail_response.data

    dashboard_response = client.get("/")
    assert b"1</strong> completed workouts" in dashboard_response.data
    assert f'/workouts/{workout_id}'.encode() in dashboard_response.data


def test_invalid_workout_log_does_not_complete_session(app, client):
    register(client)
    create_plan(client)
    with app.app_context():
        plan_id = WorkoutPlan.query.one().id

    client.post(f"/workouts/start/{plan_id}/0")
    with app.app_context():
        workout_id = WorkoutSession.query.one().id

    response = client.post(
        f"/workouts/{workout_id}/complete",
        data={"reps_0_1": "-1", "weight_0_1": "95"},
    )

    assert response.status_code == 400
    with app.app_context():
        workout = db.session.get(WorkoutSession, workout_id)
        assert workout.completed_at is None
        assert ExerciseLog.query.count() == 0
