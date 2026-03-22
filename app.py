from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#SQLite database file in project folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///firstrep.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

EXERCISE_LIBRARY = {
    "push_ups": {"name": "Push-Up", "media_file": "push_up.gif"},
    "squat": {"name": "Squat", "media_file": "squat.gif"},
    "lat_pulldown": {"name": "Lat Pulldown", "media_file": None},
    "plank": {"name": "Plank", "media_file": None},
    "deadlift": {"name": "Deadlift", "media_file": None},
    "dumbbell_bench_press": {"name": "Dumbbell Bench Press", "media_file": None},
    "seated_row": {"name": "Seated Row", "media_file": None},
    "lunges": {"name": "Lunges", "media_file": None},
    "bench_press": {"name": "Bench Press", "media_file": None},
    "shoulder_press": {"name": "Shoulder Press", "media_file": None},
    "tricep_pushdown": {"name": "Tricep Pushdown", "media_file": None},
    "bicep_curl": {"name": "Bicep Curl", "media_file": None},
    "romanian_deadlift": {"name": "Romanian Deadlift", "media_file": None},
    "calf_raise": {"name": "Calf Raise", "media_file": None},
    "incline_dumbbell_press": {"name": "Incline Dumbbell Press", "media_file": None},
    "dumbbell_press": {"name": "Dumbbell Press", "media_file": None},
    "hammer_curl": {"name": "Hammer Curl", "media_file": None},
    "goblet_squat": {"name": "Goblet Squat", "media_file": None},
    "row": {"name": "Row", "media_file": None},
    "dead_bug": {"name": "Dead Bug", "media_file": None},
    "step_up": {"name": "Step-Up", "media_file": None},
    "mountain_climbers": {"name": "Mountain Climbers", "media_file": None},
    "glute_bridge": {"name": "Glute Bridge", "media_file": None},
    "bodyweight_squat": {"name": "Bodyweight Squat", "media_file": None},
    "kettlebell_swings": {"name": "Kettlebell Swings", "media_file": None},
    "barbell_row": {"name": "Barbell Row", "media_file": None},
    "leg_press": {"name": "Leg Press", "media_file": None},
    "incline_bench_press": {"name": "Incline Bench Press", "media_file": None},
    "lateral_raise": {"name": "Lateral Raise", "media_file": None},
    "face_pull": {"name": "Face Pull", "media_file": None},
    "15_min_walk": {"name": "15-Min Walk", "media_file": None},
    "20_min_walk": {"name": "20-Min Walk", "media_file": None},
    "15_20_min_cardio": {"name": "15-20 Min Cardio", "media_file": None},
    "15_min_bike": {"name": "15-Min Bike", "media_file": None},
    "incline_walk": {"name": "Incline Walk", "media_file": None},
    "core_work": {"name": "Core Work", "media_file": None},
}

#database model for onboarding submissions
class Onboarding(db.Model):
    __tablename__ = "onboarding"

    id = db.Column(db.Integer, primary_key = True)
    #Might want to extend character count.
    goal = db.Column(db.String(100), nullable = False)
    weight = db.Column(db.Integer, nullable = False)
    days_per_week = db.Column(db.Integer, nullable = False)
    created_at = db.Column(db.DateTime, server_default = db.func.now())


#workout logic here
def generate_workout_plan(goal, days_per_week):
    if goal == "muscle_gain":
        if days_per_week == 2:
            return {
                "title": "2-Day Muscle Gain Plan",
                "days":[
                {
                "day": "Day 1",
                "focus": "Full Body A",
                "exercises": ["squat", "push_ups", "lat_pulldown", "plank"]
                },
            {
                "day": "Day 2",
                "focus": "Full Body B",
                "exercises": ["deadlift", "dumbbell_bench_press", "seated_row", "lunges"]
            }
        ]
    }
        elif days_per_week == 3:
            return {
                "title": "3-Day Muscle Gain Plan",
                "days":[
                    {
                        "day": "Day 1",
                        "focus": "Push",
                        "exercises": ["bench_press", "shoulder_press", "tricep_pushdown"]
                    },
                    {
                        "day": "Day 2",
                        "focus": "Pull",
                        "exercises": ["lat_pulldown", "seated_row", "bicep_curl"]
                    },
                    {
                        "day": "Day 3",
                        "focus": "Legs",
                        "exercises": ["squat", "romanian_deadlift", "calf_raise"]
                    }
                ]
            }
        elif days_per_week == 4:
            return {
                "title": "4-Day Muscle Gain Plan",
                "days":[
                    {
                        "day": "Day 1",
                        "focus": "Push",
                        "exercises":["bench_press", "incline_dumbbell_press", "shoulder_press", "tricep_pushdown"]
                    },
                    {
                        "day": "Day 2",
                        "focus": "Pull",
                        "exercises": ["lat_pulldown", "barbell_row", "seated_row", "bicep_curl"]
                    },
                    {
                        "day": "Day 3",
                        "focus": "Legs",
                        "exercises":["squat", "romanian_deadlift", "leg_press", "calf_raise"]
                    },
                    {
                        "day": "Day 4",
                        "focus": "Upper",
                        "exercises":["incline_bench_press", "lateral_raise", "face_pull", "hammer_curl"]
                    }
                ]
            }
        
    elif goal == "weight_loss":
        if days_per_week == 2:
            return {
                "title": "2-Day Weight Loss Plan",
                "days":[
                    {
                        "day": "Day 1",
                        "focus": "Full Body + Cardio",
                        "exercises": ["goblet_squat", "push_ups", "row", "15_min_walk"]
                    },
                    {
                        "day" : "Day 2",
                        "focus": "Full Body + Cardio",
                        "exercises":["lunges", "dumbbell_press", "lat_pulldown", "15_min_bike"]
                    }
                ]
            }
        elif days_per_week == 3:
            return {
                "title": "3-Day Weight Loss Plan",
                "days":[
                    {
                        "day": "Day 1",
                        "focus": "Upper Body",
                        "exercises": ["push_ups", "shoulder_press", "lat_pulldown"]
                    },
                    {
                        "day": "Day 2",
                        "focus": "Lower Body + Cardio",
                        "exercises": ["squat", "lunges", "20_min_walk"]                        
                    },
                    {
                        "day": "Day 3",
                        "focus": "Full Body",
                        "exercises": ["deadlift", "bench_press", "row"]
                    }
                ]
            }
        elif days_per_week == 4:
            return {
                "title": "4-Day Weight Loss Plan",
                "days":[
                    {
                        "day": "Day 1",
                        "focus": "Upper + Cardio",
                        "exercises":["push_ups", "shoulder_press","lat_pulldown", "15_20_min_cardio"]
                    },
                    {
                        "day":"Day 2",
                        "focus": "Lower + Cardio",
                        "exercises": ["squat", "lunges", "romanian_deadlift","15_20_min_cardio"]
                    },
                    {
                        "day": "Day 3",
                        "focus": "Full Body Circuit",
                        "exercises":["goblet_squat", "push_ups", "row", "plank"]
                    },
                    {
                        "day": "Day 4",
                        "focus": "Low-Impact Conditioning + Core",
                        "exercises": ["incline_walk", "dead_bug", "mountain_climbers", "plank"]
                    }
                ]
            }

        
    elif goal == "general_fitness":
        if days_per_week == 2:
            return {
                "title": "2-Day General Fitness Plan",
                "days":[
                    {
                        "day": "Day 1",
                        "focus": "Full Body A",
                        "exercises":["bodyweight_squat", "push_ups", "row", "plank"]
                    },
                    {
                        "day": "Day 2",
                        "focus": "Full Body B",
                        "exercises": ["step_up", "shoulder_press", "lat_pulldown", "dead_bug"]
                    }
                ]
            }
        elif days_per_week == 3:
            return {
                "title": "3-Day General Fitness Plan",
                "days":[
                    {
                        "day": "Day 1",
                        "focus": "Upper Body",
                        "exercises":["push_ups","shoulder_press", "row"]
                    },
                    {
                        "day": "Day 2",
                        "focus": "Lower Body",
                        "exercises": ["squat", "lunges", "glute_bridge"]
                    },
                    {
                        "day" : "Day 3",
                        "focus": "Full Body",
                        "exercises":["deadlift", "bench_press", "lat_pulldown"]
                    }
                ]
            }
        elif days_per_week == 4:
            return {
                "title": "4-Day General Fitness Plan",
                "days":[
                    {
                        "day": "Day 1",
                        "focus": "Upper Body",
                        "exercises": ["push_ups", "shoulder_press", "row", "lat_pulldown"]
                    },
                    {
                        "day": "Day 2",
                        "focus": "Lower Body",
                        "exercises":["squat", "lunges","glute_bridge","calf_raise"]
                    },
                    {
                        "day":"Day 3",
                        "focus": "Full Body",
                        "exercises": ["deadlift", "bench_press", "row", "plank"]
                    },
                    {
                        "day":"Day 4",
                        "focus": "Conditioning",
                        "exercises":["kettlebell_swings", "step_up", "push_ups", "core_work"]
                    }
                ]
            }
        
    return{
        "title": "Starter Workout Plan",
        "days":[
            {
                "day": "Day 1",
                "focus": "Full Body",
                "exercises": ["squat", "push_ups", "row", "plank"]
            }
        ]
    }



#route to home page
@app.route("/")
def home():
    recent_onboarding = Onboarding.query.order_by(Onboarding.created_at.desc()).first()
    return render_template("home.html", onboarding = recent_onboarding)

#route to workout plan page
@app.route("/workout-plan")
def workoutplan():
    recent_onboarding = Onboarding.query.order_by(Onboarding.created_at.desc()).first()
    if not recent_onboarding:
        return redirect(url_for("onboarding"))
    
    plan = generate_workout_plan(recent_onboarding.goal, recent_onboarding.days_per_week)

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
    return render_template("workout_plan.html", plan = plan, onboarding = recent_onboarding)


#route to onboarding page
@app.route("/onboarding", methods = ["GET", "POST"])
def onboarding():
    if request.method == "POST":
        goal = request.form.get("goal")
        str_weight = request.form.get("weight","").strip()
        str_days_per_week = request.form.get("days_per_week","").strip()

        VALID_GOALS ={"muscle_gain", "weight_loss", "general_fitness"}

        if not goal:
            return render_template("onboarding.html", error="Please enter a fitness goal.")
        if goal not in VALID_GOALS:
            return render_template("onboarding.html", error= "Invalid goal selected.")
        
        try:
            weight = int(str_weight)
            if weight <= 0:
                return render_template("onboarding.html", error="Please enter a valid weight.")
        except ValueError:
            return render_template("onboarding.html", error="Please enter a valid number for weight")
        
        try:
            days_per_week = int(str_days_per_week)
            if days_per_week < 1 or days_per_week > 7:
                return render_template("onboarding.html", error="Please enter a number between 1 and 7 for number of days per week.")
            
        except ValueError:
            return render_template("onboarding.html",error="Please enter a valid number for number of days per week.")
        
        new_entry = Onboarding(
            goal = goal,
            weight = weight,
            days_per_week = days_per_week
        )

        db.session.add(new_entry)
        db.session.commit()

        return redirect(url_for("workoutplan"))
    return render_template("onboarding.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)