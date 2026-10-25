Set-Content -Path README.md -Value @"
# Workout Backend API

## Description
A RESTful backend API for a workout tracking application built using Flask, SQLAlchemy, Marshmallow, and SQLite. This application allows personal trainers to create, view, and delete workouts and reusable exercises, as well as associate exercises with specific workouts using custom sets, reps, or durations.

## Installation Instructions
1. **Clone the repository:**
   \`\`\`bash
   git clone https://github.com/daniellesiamon-cpu/workout-backend-api.git
   cd workout-backend-api
   \`\`\`

2. **Install dependencies:**
   \`\`\`bash
   pipenv install
   \`\`\`

3. **Initialize and migrate the database:**
   \`\`\`bash
   flask db upgrade
   \`\`\`

4. **Seed the database:**
   \`\`\`bash
   python seed.py
   \`\`\`

## Run Instructions
Start the Flask development server:
\`\`\`bash
python app.py
\`\`\`
The API will run locally on \`http://127.0.0.1:5555\`.

## API Endpoints

### Workouts
- \`GET /workouts\` - Retrieve all workouts with nested exercises.
- \`GET /workouts/<id>\` - Retrieve a single workout by ID.
- \`POST /workouts\` - Create a new workout.
- \`DELETE /workouts/<id>\` - Delete a workout by ID.

### Exercises
- \`GET /exercises\` - Retrieve all available exercises.
- \`POST /exercises\` - Create a new exercise.
- \`DELETE /exercises/<id>\` - Delete an exercise by ID.

### Workout Exercises
- \`POST /workouts/<id>/exercises\` - Associate an exercise with a workout (includes sets, reps, or duration).
"@