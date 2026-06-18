# FirstRep

FirstRep is a full-stack fitness web application that generates personalized beginner workout plans based on a user's fitness goal, weight, and preferred training frequency. Users can create an account, complete onboarding, generate a workout plan, and return later to view their saved plan.

Live Demo: https://firstrep-uaym.onrender.com

## Tech Stack

- Python
- Flask
- SQLAlchemy
- PostgreSQL
- HTML/CSS
- Jinja
- Render

## Features

- User registration and login
- Personalized onboarding flow
- Workout plan generation based on user inputs
- Persistent storage of user profiles, onboarding data, and workout plans
- Saved workout plan retrieval
- Exercise media integration for visual guidance
- Multi-page Flask application with dynamic routing
- Deployed with Render and PostgreSQL

## How It Works

1. A user creates an account or logs in.
2. The user completes an onboarding form with their goal, weight, and training frequency.
3. FirstRep generates a structured workout plan based on the user's inputs.
4. The generated plan is saved to the database.
5. The user can return later and view their most recent saved workout plan.

## Project Motivation

Many beginners struggle with knowing what to do when they first start going to the gym. FirstRep is designed to reduce that uncertainty by giving users a simple, personalized starting point. The goal is not to replace a trainer, but to help new gym-goers build confidence with an accessible workout plan.

## Current Limitations

- Workout generation is currently rule-based.
- Exercise selection is limited to a beginner-focused library.
- UI/UX is functional but still being improved.
- User accounts currently store the most recent onboarding and workout plan.

## Future Improvements

- Add more advanced workout generation logic
- Support equipment constraints such as home workouts, dumbbells only, or no machines
- Expand the exercise library
- Improve UI/UX and mobile responsiveness
- Add user dashboards and workout history
- Add profile editing and account management
- Add API documentation and tests

## Running Locally

Clone the repository:

```bash
git clone <your-repo-url>
cd FirstRep
