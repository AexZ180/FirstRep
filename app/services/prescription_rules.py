PRESCRIPTION_RULES = {
    "muscle_gain": {
        "compound": {
            "sets": 4,
            "reps": "6-10",
            "rest": "90-120 sec",
            "notes": "Use a challenging weight while leaving 1-2 reps in reserve.",
        },
        "isolation": {
            "sets": 3,
            "reps": "10-15",
            "rest": "45-75 sec",
            "notes": "Control the movement and focus on the target muscle.",
        },
        "core": {
            "sets": 3,
            "reps": "30-45 sec",
            "rest": "45 sec",
            "notes": "Keep your trunk braced and stop if form breaks down.",
        },
        "cardio": {
            "sets": 1,
            "reps": "10-15 min",
            "rest": "as needed",
            "notes": "Keep the pace moderate so it supports your strength work.",
        },
    },
    "weight_loss": {
        "compound": {
            "sets": 3,
            "reps": "10-15",
            "rest": "45-60 sec",
            "notes": "Move steadily and keep rest periods controlled.",
        },
        "isolation": {
            "sets": 2,
            "reps": "12-15",
            "rest": "30-45 sec",
            "notes": "Use smooth reps without rushing the exercise.",
        },
        "core": {
            "sets": 3,
            "reps": "30-45 sec",
            "rest": "30-45 sec",
            "notes": "Focus on steady breathing and clean form.",
        },
        "cardio": {
            "sets": 1,
            "reps": "15-25 min",
            "rest": "as needed",
            "notes": "Aim for a pace where talking is possible but slightly difficult.",
        },
    },
    "general_fitness": {
        "compound": {
            "sets": 3,
            "reps": "8-12",
            "rest": "60-90 sec",
            "notes": "Choose a weight or variation you can control well.",
        },
        "isolation": {
            "sets": 2,
            "reps": "10-15",
            "rest": "45-60 sec",
            "notes": "Prioritize range of motion over heavier weight.",
        },
        "core": {
            "sets": 3,
            "reps": "30 sec",
            "rest": "45 sec",
            "notes": "Brace your core and keep each rep deliberate.",
        },
        "cardio": {
            "sets": 1,
            "reps": "10-20 min",
            "rest": "as needed",
            "notes": "Keep the intensity comfortable and repeatable.",
        },
    },
}


def get_prescription_rules(goal, movement):
    goal_rules = PRESCRIPTION_RULES.get(goal, PRESCRIPTION_RULES["general_fitness"])
    return goal_rules.get(movement, goal_rules["compound"])
