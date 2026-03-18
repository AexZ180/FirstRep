from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#SQLite database file in project folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///firstrep.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

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
                "exercises": [
                    {"name": "Squat", "link":"https://tenor.com/view/barbellsquats-gymexercisesmen-gif-5038916500459247573"},
                    {"name": "Push-Up", "link": "https://tenor.com/view/flexiones-basicas-gif-1171585521907987152"}
                    {"name": "Lat Pulldown", "link": "https://tenor.com/view/pulley-pegada-aberta-gif-4419295319283270407"}
                    {"name": "Plank", "link": "https://tenor.com/view/plank-gif-17072734464850924730"}
                    ]
                },
            {
                "day": "Day 2",
                "focus": "Full Body B",
                "exercises": [
                    {"name":"Deadlift", "link":"https://tenor.com/view/gym-gif-6044559530521560855"}
                    {"name:":"Dumbbell Bench Press", "link":"https://tenor.com/view/supino-reto-gif-11462340842717886275"}
                    {"name:":"Seated Row", "link":"https://tenor.com/view/seated-row-gif-15624707278175899735"}
                    {"name:":"Lunges", "link":"https://tenor.com/view/afundo-com-halteres-gif-13923904176810813441"}
                ]
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
                        "exercises": ["Bench Press", "Shoulder Press", "Tricep Pushdown"]
                    },
                    {
                        "day": "Day 2",
                        "focus": "Pull",
                        "exercises": ["Lat Pulldown", "Seated Row", "Bicep Curl"]
                    },
                    {
                        "day": "Day 3",
                        "focus": "Legs",
                        "exercises": ["Squat", "Romanian Deadlift", "Calf Raise"]
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
                        "exercises":["Bench Press", "Incline Dumbbell Press", "Shoulder Press", "Tricep Pushdown"]
                    },
                    {
                        "day": "Day 2",
                        "focus": "Pull",
                        "exercises": ["Lat Pulldown", "Barbell Row", "Seated Row", "Bicep Curl"]
                    },
                    {
                        "day": "Day 3",
                        "focus": "Legs",
                        "exercises":["Squat", "Romanian Deadlift", "Leg Press", "Calf Raise"]
                    },
                    {
                        "day": "Day 4",
                        "focus": "Upper",
                        "exercises":["Incline Bench Press", "Lateral Raise", "Face Pull", "Hammer Curl"]
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
                        "exercises": ["Goblet Squat", "Push-Up", "Row", "15-Min Walk"]
                    },
                    {
                        "day" : "Day 2",
                        "focus": "Full Body + Cardio",
                        "exercises":["Lunge", "Dumbbell Press", "Lat Pulldown", "15-Min Bike"]
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
                        "exercises": ["Push-Up", "Shoulder Press", "Lat Pulldown"]
                    },
                    {
                        "day": "Day 2",
                        "focus": "Lower Body + Cardio",
                        "exercises": ["Squat", "Lunge", "20-Min Walk"]                        
                    },
                    {
                        "day": "Day 3",
                        "focus": "Full Body",
                        "exercises": ["Deadlift", "Bench Press", "Row"]
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
                        "exercises":["Push-Up", "Shoulder Press","Lat Pulldown", "15-20 Min Cardio"]
                    },
                    {
                        "day":"Day 2",
                        "focus": "Lower + Cardio",
                        "exercises": ["Squat", "Lunge", "Romanian Deadlift","15-20 Min Cardio"]
                    },
                    {
                        "day": "Day 3",
                        "focus": "Full Body Circuit",
                        "exercises":["Goblet Squat", "Push-Up", "Row", "Plank"]
                    },
                    {
                        "day": "Day 4",
                        "focus": "Low-Impact Conditioning + Core",
                        "exercises": ["Incline Walk", "Dead Bug", "Mountain Climbers", "Plank"]
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
                        "exercises":["Bodyweight Squat", "Push-Up", "Row", "Plank"]
                    },
                    {
                        "day": "Day 2",
                        "focus": "Full Body B",
                        "exercises": ["Step-Up", "Shoulder Press", "Lat Pulldown", "Dead Bug"]
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
                        "exercises":["Push-Up","Shoulder Press", "Row"]
                    },
                    {
                        "day": "Day 2",
                        "focus": "Lower Body",
                        "exercises": ["Squat", "Lunge", "Glute Bridge"]
                    },
                    {
                        "day" : "Day 3",
                        "focus": "Full Body",
                        "exercises":["Deadlift", "Bench Press", "Lat Pulldown"]
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
                        "exercises": ["Push-Up", "Shoulder Press", "Row", "Lat Pulldown"]
                    },
                    {
                        "day": "Day 2",
                        "focus": "Lower Body",
                        "exercises":["Squat", "Lunge","Glute Bridge","Calf Raise"]
                    },
                    {
                        "day":"Day 3",
                        "focus": "Full Body",
                        "exercises": ["Deadlift", "Bench Press", "Row", "Plank"]
                    },
                    {
                        "day":"Day 4",
                        "focus": "Conditioning",
                        "exercises":["Kettlebell Swings", "Step-Ups", "Push-Ups", "Core Work"]
                    }
                ]
            }
        
    return{
        "title": "Starter Workout Plan",
        "days":[
            {
                "day": "Day 1",
                "focus": "Full Body",
                "exercises": ["Squat", "Push-Up", "Row", "Plank"]
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