import json
from flask import Blueprint, render_template, url_for, redirect

from app.data.exercise_library import EXERCISE_LIBRARY
from app.models import Onboarding, WorkoutPlan

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    recent_onboarding = Onboarding.query.order_by(Onboarding.created_at.desc()).first()
    recent_saved_plan = WorkoutPlan.query.order_by(WorkoutPlan.created_at.desc()).first()

    plan = None
    if recent_saved_plan:
        plan = json.loads(recent_saved_plan.plan_json)

    return render_template("home.html", onboarding=recent_onboarding, plan=plan)


@main_bp.route("/workout-plan")
def workoutplan():
    recent_onboarding = Onboarding.query.order_by(Onboarding.created_at.desc()).first()
    if not recent_onboarding:
        return redirect(url_for("onboarding.onboarding"))

    saved_plan = (
        WorkoutPlan.query.filter_by(onboarding_id=recent_onboarding.id)
        .order_by(WorkoutPlan.created_at.desc())
        .first()
    )

    if not saved_plan:
        return redirect(url_for("onboarding.onboarding"))

    plan = json.loads(saved_plan.plan_json)

    for day in plan["days"]:
        new_exercises = []
        for ex in day["exercises"]:
            if ex not in EXERCISE_LIBRARY:
                raise ValueError(f"Invalid exercise key: {ex}")

            exercise_data = EXERCISE_LIBRARY[ex].copy()
            media_file = exercise_data.get("media_file")

            if media_file:
                exercise_data["media_url"] = url_for("static", filename=f"gifs/{media_file}")
            else:
                exercise_data["media_url"] = ""

            new_exercises.append(exercise_data)

        day["exercises"] = new_exercises

    return render_template("workout_plan.html", plan=plan, onboarding=recent_onboarding)