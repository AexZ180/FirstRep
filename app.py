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

#route to home page
@app.route("/")
def home():
    recent_onboarding = Onboarding.query.order_by(Onboarding.created_at.desc()).first()
    return render_template("home.html", onboarding = recent_onboarding)

#route to onboarding page
@app.route("/onboarding", methods = ["GET", "POST"])
def onboarding():
    if request.method == "POST":
        goal = request.form.get("goal")
        str_weight = request.form.get("weight","").strip()
        str_days_per_week = request.form.get("days_per_week","").strip()

        VALID_GOALS ={"muscle_gain", "weight_loss", "general_fit"}

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

        return redirect(url_for("home"))
    return render_template("onboarding.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)