from .extensions import db

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    onboardings = db.relationship("Onboarding", backref="user", lazy=True)
    workout_sessions = db.relationship(
        "WorkoutSession",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan",
    )


class Onboarding(db.Model):
    __tablename__ = "onboarding"

    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    days_per_week = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class WorkoutPlan(db.Model):
    __tablename__ = "workout_plan"

    id = db.Column(db.Integer, primary_key=True)
    onboarding_id = db.Column(db.Integer, db.ForeignKey("onboarding.id"), nullable=False)
    plan_json = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    workout_sessions = db.relationship(
        "WorkoutSession",
        backref="workout_plan",
        lazy=True,
        cascade="all, delete-orphan",
    )


class WorkoutSession(db.Model):
    __tablename__ = "workout_session"
    __table_args__ = (
        db.CheckConstraint("day_index >= 0", name="ck_session_day_index_nonnegative"),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    workout_plan_id = db.Column(
        db.Integer,
        db.ForeignKey("workout_plan.id"),
        nullable=False,
    )
    day_index = db.Column(db.Integer, nullable=False)
    started_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)

    exercise_logs = db.relationship(
        "ExerciseLog",
        backref="workout_session",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="ExerciseLog.id",
    )


class ExerciseLog(db.Model):
    __tablename__ = "exercise_log"
    __table_args__ = (
        db.CheckConstraint("set_number > 0", name="ck_log_set_number_positive"),
        db.CheckConstraint("reps >= 0", name="ck_log_reps_nonnegative"),
        db.CheckConstraint("weight >= 0", name="ck_log_weight_nonnegative"),
        db.UniqueConstraint(
            "workout_session_id",
            "exercise_key",
            "set_number",
            name="uq_log_session_exercise_set",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    workout_session_id = db.Column(
        db.Integer,
        db.ForeignKey("workout_session.id"),
        nullable=False,
    )
    exercise_key = db.Column(db.String(100), nullable=False)
    set_number = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=True)
    weight = db.Column(db.Float, nullable=True)
