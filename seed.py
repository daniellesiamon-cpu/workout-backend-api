from app import app
from models import db, Workout, Exercise, WorkoutExercise

with app.app_context():
    print("Clearing database...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    print("Seeding exercises...")
    ex1 = Exercise(name="Bench Press", category="Strength", muscle_group="Chest")
    ex2 = Exercise(name="Squat", category="Strength", muscle_group="Legs")
    ex3 = Exercise(name="Treadmill Run", category="Cardio", muscle_group="Full Body")
    db.session.add_all([ex1, ex2, ex3])
    db.session.commit()

    print("Seeding workouts...")
    w1 = Workout(name="Leg Day Heavy", date="2026-10-25", duration_minutes=60)
    w2 = Workout(name="Morning Cardio", date="2026-10-26", duration_minutes=30)
    db.session.add_all([w1, w2])
    db.session.commit()

    print("Adding exercises to workouts...")
    we1 = WorkoutExercise(workout_id=w1.id, exercise_id=ex2.id, sets=4, reps=10)
    we2 = WorkoutExercise(workout_id=w2.id, exercise_id=ex3.id, duration_seconds=1800)
    db.session.add_all([we1, we2])
    db.session.commit()

    print("Database successfully seeded!")
