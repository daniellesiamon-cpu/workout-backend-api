from flask_marshmallow import Marshmallow
from marshmallow import fields, validate, validates, ValidationError
from models import Workout, Exercise, WorkoutExercise

ma = Marshmallow()

class ExerciseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Exercise
        load_instance = True

    name = fields.String(required=True, validate=validate.Length(min=2, max=100))
    category = fields.String(required=True)
    muscle_group = fields.String(required=True, validate=validate.Length(min=2))


class WorkoutExerciseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WorkoutExercise
        load_instance = True
        include_fk = True

    exercise = fields.Nested(ExerciseSchema, dump_only=True)
    sets = fields.Integer(required=False, validate=validate.Range(min=1))
    reps = fields.Integer(required=False, validate=validate.Range(min=1))


class WorkoutSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Workout
        load_instance = True

    name = fields.String(required=True, validate=validate.Length(min=3))
    duration_minutes = fields.Integer(required=True, validate=validate.Range(min=1, max=300))
    workout_exercises = fields.Nested(WorkoutExerciseSchema, many=True, dump_only=True)

    @validates('name')
    def validate_workout_name(self, value):
        if "test" in value.lower():
            raise ValidationError("Workout name cannot contain 'test'.")


workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()
