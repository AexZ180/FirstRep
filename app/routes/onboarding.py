import json
from flask import Blueprint, render_template, request, url_for, redirect

from app.extensions import db
from app.models import Onboarding, WorkoutPlan
from app.services.workout_generator import generate_workout_plan

onboarding_bp = Blueprint("onboarding", __name__)

@onboarding_bp.route("/onboarding", methods=["GET", "POST"])
def onboarding():
    if request.method == "POST":
        goal = request.form.get("goal")
        str_weight = request.form.get("weight", "").strip()
        str_days_per_week = request.form.get("days_per_week", "").strip()

        valid_goals = {"muscle_gain", "weight_loss", "general_fitness"}

        if not goal:
            return render_template("onboarding.html", error="Please enter a fitness goal.")
        if goal not in valid_goals:
            return render_template("onboarding.html", error="Invalid goal selected.")

        try:
            weight = int(str_weight)
            if weight <= 0:
                return render_template("onboarding.html", error="Please enter a valid weight.")
        except ValueError:
            return render_template("onboarding.html", error="Please enter a valid number for weight.")

        try:
            days_per_week = int(str_days_per_week)
            if days_per_week < 1 or days_per_week > 7:
                return render_template(
                    "onboarding.html",
                    error="Please enter a number between 1 and 7 for number of days per week."
                )
        except ValueError:
            return render_template(
                "onboarding.html",
                error="Please enter a valid number for number of days per week."
            )

        new_entry = Onboarding(
            goal=goal,
            weight=weight,
            days_per_week=days_per_week
        )

        db.session.add(new_entry)
        db.session.commit()

        plan = generate_workout_plan(goal, days_per_week)

        saved_plan = WorkoutPlan(
            onboarding_id=new_entry.id,
            plan_json=json.dumps(plan)
        )

        db.session.add(saved_plan)
        db.session.commit()

        return redirect(url_for("main.workoutplan"))

    return render_template("onboarding.html")