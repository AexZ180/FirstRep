from flask import Flask, render_template, request
app = Flask(__name__)

@app.get("/")
def home():
    return render_template("home.html")

@app.route("/onboarding", methods = ["GET","POST"])
def onboarding():
    if request.method == "POST":
        # Process the form data and create a workout plan
        print("Workout plan created!")

    return render_template("onboarding.html")

if __name__ == "__main__":
    app.run(debug=True)