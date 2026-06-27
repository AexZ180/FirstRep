from app.data.exercise_library import EXERCISE_LIBRARY
from app.services.prescription_rules import get_prescription_rules


def build_exercise(exercise_key, goal):
    exercise = EXERCISE_LIBRARY[exercise_key]
    prescription = get_prescription_rules(goal, exercise["movement"])

    return {
        "key": exercise_key,
        "sets": prescription["sets"],
        "reps": prescription["reps"],
        "rest": prescription["rest"],
        "notes": prescription["notes"],
    }


def build_plan(title, days, goal):
    return {
        "title": title,
        "days": [
            {
                "day": day["day"],
                "focus": day["focus"],
                "exercises": [
                    build_exercise(exercise_key, goal)
                    for exercise_key in day["exercise_keys"]
                ],
            }
            for day in days
        ],
    }


def generate_workout_plan(goal, days_per_week):
    if goal == "muscle_gain":
        if days_per_week == 2:
            return build_plan(
                "2-Day Muscle Gain Plan",
                [
                    {
                        "day": "Day 1",
                        "focus": "Full Body A",
                        "exercise_keys": ["squat", "push_ups", "lat_pulldown", "plank"],
                    },
                    {
                        "day": "Day 2",
                        "focus": "Full Body B",
                        "exercise_keys": ["deadlift", "dumbbell_bench_press", "seated_row", "lunges"],
                    },
                ],
                goal,
            )
        elif days_per_week == 3:
            return build_plan(
                "3-Day Muscle Gain Plan",
                [
                    {
                        "day": "Day 1",
                        "focus": "Push",
                        "exercise_keys": ["bench_press", "shoulder_press", "tricep_pushdown"],
                    },
                    {
                        "day": "Day 2",
                        "focus": "Pull",
                        "exercise_keys": ["lat_pulldown", "seated_row", "bicep_curl"],
                    },
                    {
                        "day": "Day 3",
                        "focus": "Legs",
                        "exercise_keys": ["squat", "romanian_deadlift", "calf_raise"],
                    },
                ],
                goal,
            )
        elif days_per_week == 4:
            return build_plan(
                "4-Day Muscle Gain Plan",
                [
                    {
                        "day": "Day 1",
                        "focus": "Push",
                        "exercise_keys": ["bench_press", "incline_dumbbell_press", "shoulder_press", "tricep_pushdown"],
                    },
                    {
                        "day": "Day 2",
                        "focus": "Pull",
                        "exercise_keys": ["lat_pulldown", "barbell_row", "seated_row", "bicep_curl"],
                    },
                    {
                        "day": "Day 3",
                        "focus": "Legs",
                        "exercise_keys": ["squat", "romanian_deadlift", "leg_press", "calf_raise"],
                    },
                    {
                        "day": "Day 4",
                        "focus": "Upper",
                        "exercise_keys": ["incline_bench_press", "lateral_raise", "face_pull", "hammer_curl"],
                    },
                ],
                goal,
            )

    elif goal == "weight_loss":
        if days_per_week == 2:
            return build_plan(
                "2-Day Weight Loss Plan",
                [
                    {
                        "day": "Day 1",
                        "focus": "Full Body + Cardio",
                        "exercise_keys": ["goblet_squat", "push_ups", "row", "15_min_walk"],
                    },
                    {
                        "day": "Day 2",
                        "focus": "Full Body + Cardio",
                        "exercise_keys": ["lunges", "dumbbell_press", "lat_pulldown", "15_min_bike"],
                    },
                ],
                goal,
            )
        elif days_per_week == 3:
            return build_plan(
                "3-Day Weight Loss Plan",
                [
                    {
                        "day": "Day 1",
                        "focus": "Upper Body",
                        "exercise_keys": ["push_ups", "shoulder_press", "lat_pulldown"],
                    },
                    {
                        "day": "Day 2",
                        "focus": "Lower Body + Cardio",
                        "exercise_keys": ["squat", "lunges", "20_min_walk"],
                    },
                    {
                        "day": "Day 3",
                        "focus": "Full Body",
                        "exercise_keys": ["deadlift", "bench_press", "row"],
                    },
                ],
                goal,
            )
        elif days_per_week == 4:
            return build_plan(
                "4-Day Weight Loss Plan",
                [
                    {
                        "day": "Day 1",
                        "focus": "Upper + Cardio",
                        "exercise_keys": ["push_ups", "shoulder_press", "lat_pulldown", "15_20_min_cardio"],
                    },
                    {
                        "day": "Day 2",
                        "focus": "Lower + Cardio",
                        "exercise_keys": ["squat", "lunges", "romanian_deadlift", "15_20_min_cardio"],
                    },
                    {
                        "day": "Day 3",
                        "focus": "Full Body Circuit",
                        "exercise_keys": ["goblet_squat", "push_ups", "row", "plank"],
                    },
                    {
                        "day": "Day 4",
                        "focus": "Low-Impact Conditioning + Core",
                        "exercise_keys": ["incline_walk", "dead_bug", "mountain_climbers", "plank"],
                    },
                ],
                goal,
            )

    elif goal == "general_fitness":
        if days_per_week == 2:
            return build_plan(
                "2-Day General Fitness Plan",
                [
                    {
                        "day": "Day 1",
                        "focus": "Full Body A",
                        "exercise_keys": ["bodyweight_squat", "push_ups", "row", "plank"],
                    },
                    {
                        "day": "Day 2",
                        "focus": "Full Body B",
                        "exercise_keys": ["step_up", "shoulder_press", "lat_pulldown", "dead_bug"],
                    },
                ],
                goal,
            )
        elif days_per_week == 3:
            return build_plan(
                "3-Day General Fitness Plan",
                [
                    {
                        "day": "Day 1",
                        "focus": "Upper Body",
                        "exercise_keys": ["push_ups", "shoulder_press", "row"],
                    },
                    {
                        "day": "Day 2",
                        "focus": "Lower Body",
                        "exercise_keys": ["squat", "lunges", "glute_bridge"],
                    },
                    {
                        "day": "Day 3",
                        "focus": "Full Body",
                        "exercise_keys": ["deadlift", "bench_press", "lat_pulldown"],
                    },
                ],
                goal,
            )
        elif days_per_week == 4:
            return build_plan(
                "4-Day General Fitness Plan",
                [
                    {
                        "day": "Day 1",
                        "focus": "Upper Body",
                        "exercise_keys": ["push_ups", "shoulder_press", "row", "lat_pulldown"],
                    },
                    {
                        "day": "Day 2",
                        "focus": "Lower Body",
                        "exercise_keys": ["squat", "lunges", "glute_bridge", "calf_raise"],
                    },
                    {
                        "day": "Day 3",
                        "focus": "Full Body",
                        "exercise_keys": ["deadlift", "bench_press", "row", "plank"],
                    },
                    {
                        "day": "Day 4",
                        "focus": "Conditioning",
                        "exercise_keys": ["kettlebell_swings", "step_up", "push_ups", "core_work"],
                    },
                ],
                goal,
            )

    return build_plan(
        "Starter Workout Plan",
        [
            {
                "day": "Day 1",
                "focus": "Full Body",
                "exercise_keys": ["squat", "push_ups", "row", "plank"],
            }
        ],
        "general_fitness",
    )
