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
