from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Workout(db.Model):
    __tablename__ = 'workouts'

    # Table Constraint
    __table_args__ = (
        CheckConstraint('duration_minutes > 0', name='check_workout_duration_positive'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)

    # Relationships
    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan')

    # Model Validation 1
    @validates('name')
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Workout name cannot be empty.")
        return value.strip()


class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)  # Table Constraint: unique=True
    category = db.Column(db.String(50), nullable=False)
    muscle_group = db.Column(db.String(50), nullable=False)

    # Relationships
    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan')

    # Model Validation 2
    @validates('category')
    def validate_category(self, key, value):
        allowed_categories = ['Strength', 'Cardio', 'Flexibility', 'Balance']
        if value not in allowed_categories:
            raise ValueError(f"Category must be one of: {', '.join(allowed_categories)}")
        return value


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    # Table Constraints
    __table_args__ = (
        CheckConstraint('sets >= 1', name='check_sets_positive'),
        CheckConstraint('reps >= 1', name='check_reps_positive'),
    )

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    sets = db.Column(db.Integer, nullable=True)
    reps = db.Column(db.Integer, nullable=True)
    duration_seconds = db.Column(db.Integer, nullable=True)

    # Relationships
    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')
