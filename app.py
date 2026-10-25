from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Workout, Exercise, WorkoutExercise
from schemas import (
    ma, workout_schema, workouts_schema, 
    exercise_schema, exercises_schema, workout_exercise_schema
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
ma.init_app(app)
migrate = Migrate(app, db)

# --- WORKOUT ENDPOINTS ---

@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(workouts)), 200

@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get_or_404(id)
    return jsonify(workout_schema.dump(workout)), 200

@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json()
    errors = workout_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    new_workout = Workout(
        name=data['name'],
        date=data['date'],
        duration_minutes=data['duration_minutes']
    )
    db.session.add(new_workout)
    db.session.commit()
    return jsonify(workout_schema.dump(new_workout)), 201

@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get_or_404(id)
    db.session.delete(workout)
    db.session.commit()
    return jsonify({"message": f"Workout {id} deleted successfully."}), 200


# --- EXERCISE ENDPOINTS ---

@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(exercises)), 200

@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json()
    errors = exercise_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    try:
        new_exercise = Exercise(
            name=data['name'],
            category=data['category'],
            muscle_group=data['muscle_group']
        )
        db.session.add(new_exercise)
        db.session.commit()
        return jsonify(exercise_schema.dump(new_exercise)), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    db.session.delete(exercise)
    db.session.commit()
    return jsonify({"message": f"Exercise {id} deleted successfully."}), 200


# --- ASSOCIATE EXERCISE TO WORKOUT ---

@app.route('/workouts/<int:id>/exercises', methods=['POST'])
def add_exercise_to_workout(id):
    workout = Workout.query.get_or_404(id)
    data = request.get_json()

    errors = workout_exercise_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    exercise_id = data.get('exercise_id')
    exercise = Exercise.query.get_or_404(exercise_id)

    workout_exercise = WorkoutExercise(
        workout_id=workout.id,
        exercise_id=exercise.id,
        sets=data.get('sets'),
        reps=data.get('reps'),
        duration_seconds=data.get('duration_seconds')
    )
    db.session.add(workout_exercise)
    db.session.commit()

    return jsonify(workout_exercise_schema.dump(workout_exercise)), 201

if __name__ == '__main__':
    app.run(port=5555, debug=True)
