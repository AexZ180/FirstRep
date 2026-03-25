from .extensions import db

class Onboarding(db.Model):
    __tablename__ = "onboarding"

    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    days_per_week = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())


class WorkoutPlan(db.Model):
    __tablename__ = "workout_plan"

    id = db.Column(db.Integer, primary_key=True)
    onboarding_id = db.Column(db.Integer, db.ForeignKey("onboarding.id"), nullable=False)
    plan_json = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())