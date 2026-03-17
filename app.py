
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#SQLite database file in project folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://firstrep.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

def init_db():
    # Initialize the database and create the necessary tables
    con = get_db_connection()
    cursor = con.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            goal TEXT NOT NULL,
            weight INTEGER NOT NULL,
            days_per_week INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    con.commit()
    con.close()

@app.get("/")
def home():
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("""
        SELECT goal, weight, days_per_week FROM onboarding ORDER BY created_at DESC LIMIT 1
                """)
    row = cur.fetchone()
    con.close()
    return render_template("home.html", onboarding=row)

@app.route("/onboarding", methods = ["GET","POST"])
def onboarding():
    if request.method == "POST":
        goal = request.form.get("goal", "")
        weight_raw = request.form.get("weight", "")
        days_per_week_raw = request.form.get("days_per_week", "")

        if not goal:
            return render_template("onboarding.html", error= "Please select a fitness goal.")
        try:
            weight = int(weight_raw)
        except ValueError:
            return render_template("onboarding.html", error="Please enter valid numbers for weight.")
        
        try:
            days_per_week = int(days_per_week_raw)
            if(days_per_week < 1 or days_per_week > 7):
                return render_template("onboarding.html", error="Please enter a number between 1 and 7 for days per week.")
        except ValueError:
            return render_template("onboarding.html", error="Please enter valid numbers for days per week.")
        
        con = get_db_connection()
        cur = con.cursor()
        cur.execute("""
            INSERT INTO users (goal, weight, days_per_week) VALUES (?, ?, ?)
        """, (goal, weight, days_per_week))
        con.commit()
        con.close()

        return redirect(url_for("home"))
        # Process the form data and create a workout plan

    return render_template("onboarding.html")

if __name__ == "__main__":
    init_db()  # Initialize the database before running the app
    app.run(debug=True)