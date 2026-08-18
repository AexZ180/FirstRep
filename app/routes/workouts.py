import json

from flask import Blueprint, abort, redirect, render_template, request, session, url_for

from app.auth_utils import login_required
from app.data.exercise_library import EXERCISE_LIBRARY
from app.extensions import db
from app.models import ExerciseLog, Onboarding, WorkoutPlan, WorkoutSession

workouts_bp = Blueprint("workouts", __name__, url_prefix="/workouts")


def get_user_plan_or_404(plan_id, user_id):
    return (
        WorkoutPlan.query.join(Onboarding)
        .filter(WorkoutPlan.id == plan_id, Onboarding.user_id == user_id)
        .first_or_404()
    )


def get_user_workout_or_404(workout_id, user_id):
    return WorkoutSession.query.filter_by(
        id=workout_id,
        user_id=user_id,
    ).first_or_404()


def get_workout_day(workout):
    plan = json.loads(workout.workout_plan.plan_json)
    return plan["days"][workout.day_index]


def enrich_exercises(day):
    exercises = []
    for planned_exercise in day["exercises"]:
        exercise_key = planned_exercise["key"]
        exercise = EXERCISE_LIBRARY[exercise_key].copy()
        exercise.update(planned_exercise)
        exercises.append(exercise)
    return exercises


@workouts_bp.route("/start/<int:plan_id>/<int:day_index>", methods=["POST"])
@login_required
def start(plan_id, day_index):
    user_id = session["user_id"]
    workout_plan = get_user_plan_or_404(plan_id, user_id)
    plan = json.loads(workout_plan.plan_json)

    if day_index < 0 or day_index >= len(plan["days"]):
        abort(404)

    workout = WorkoutSession(
        user_id=user_id,
        workout_plan_id=workout_plan.id,
        day_index=day_index,
    )
    db.session.add(workout)
    db.session.commit()

    return redirect(url_for("workouts.detail", workout_id=workout.id))


@workouts_bp.route("/<int:workout_id>")
@login_required
def detail(workout_id):
    workout = get_user_workout_or_404(workout_id, session["user_id"])
    day = get_workout_day(workout)
    logs_by_set = {
        (log.exercise_key, log.set_number): log
        for log in workout.exercise_logs
    }

    return render_template(
        "workout_session.html",
        workout=workout,
        day=day,
        exercises=enrich_exercises(day),
        logs_by_set=logs_by_set,
    )


@workouts_bp.route("/<int:workout_id>/complete", methods=["POST"])
@login_required
def complete(workout_id):
    workout = get_user_workout_or_404(workout_id, session["user_id"])
    if workout.completed_at is not None:
        abort(409)

    day = get_workout_day(workout)
    logs = []

    for exercise_index, exercise in enumerate(day["exercises"]):
        for set_number in range(1, exercise["sets"] + 1):
            reps_raw = request.form.get(
                f"reps_{exercise_index}_{set_number}",
                "",
            ).strip()
            weight_raw = request.form.get(
                f"weight_{exercise_index}_{set_number}",
                "",
            ).strip()

            if not reps_raw and not weight_raw:
                continue

            try:
                reps = int(reps_raw) if reps_raw else None
                weight = float(weight_raw) if weight_raw else None
            except ValueError:
                return render_template(
                    "workout_session.html",
                    workout=workout,
                    day=day,
                    exercises=enrich_exercises(day),
                    logs_by_set={},
                    error="Reps and weight must be valid numbers.",
                ), 400

            if (reps is not None and reps < 0) or (weight is not None and weight < 0):
                return render_template(
                    "workout_session.html",
                    workout=workout,
                    day=day,
                    exercises=enrich_exercises(day),
                    logs_by_set={},
                    error="Reps and weight cannot be negative.",
                ), 400

            logs.append(
                ExerciseLog(
                    workout_session_id=workout.id,
                    exercise_key=exercise["key"],
                    set_number=set_number,
                    reps=reps,
                    weight=weight,
                )
            )

    if not logs:
        return render_template(
            "workout_session.html",
            workout=workout,
            day=day,
            exercises=enrich_exercises(day),
            logs_by_set={},
            error="Log at least one set before completing your workout.",
        ), 400

    db.session.add_all(logs)
    workout.completed_at = db.func.now()
    db.session.commit()

    return redirect(url_for("workouts.detail", workout_id=workout.id))
