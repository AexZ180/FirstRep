import json
from flask import Blueprint, render_template, url_for, redirect, session

from app.data.exercise_library import EXERCISE_LIBRARY
from app.models import Onboarding, WorkoutPlan

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("auth.login"))
    
    user_onboarding = (
        Onboarding.query.filter_by(user_id = user_id)
        .order_by(Onboarding.created_at.desc())
        .first()
    )
    saved_plan = None
    plan = None
    if user_onboarding:
        saved_plan = (
            WorkoutPlan.query.filter_by(onboarding_id=user_onboarding.id)
            .order_by(WorkoutPlan.created_at.desc())
            .first()
        )
    if saved_plan:
        plan = json.loads(saved_plan.plan_json)

    return render_template("home.html", onboarding=user_onboarding, plan=plan)


@main_bp.route("/workout-plan")
def workoutplan():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("auth.login"))
    
    user_onboarding = (
        Onboarding.query.filter_by(user_id = user_id)
        .order_by(Onboarding.created_at.desc())
        .first()
    )

    if not user_onboarding:
        return redirect(url_for("onboarding.onboarding"))
    saved_plan = (
        WorkoutPlan.query.filter_by(onboarding_id = user_onboarding.id)
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

    return render_template("workout_plan.html", plan=plan, onboarding=user_onboarding)