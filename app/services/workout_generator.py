
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
