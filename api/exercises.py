"""
This module defines an API for generating personalized exercise plans using FastAPI.
It includes endpoints to retrieve a list of exercises, get exercise details,
and create a custom exercise plan based on user profiles.
"""

from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class Exercise(BaseModel):
    name: str
    description: str
    instructions: str
    benefits: str

class UserProfile(BaseModel):
    weight: float
    height: float
    age: int
    goals: Optional[List[str]] = None
    special_health_conditions: Optional[List[str]] = None
    health_monitoring_integration: Optional[bool] = False
    progress_tracking: Optional[bool] = False

class ExercisePlan(BaseModel):
    name: str
    description: str
    exercises: List[Exercise]
    personalized: bool = True
    health_monitoring_integration: bool
    progress_tracking: bool

exercises = [
    Exercise(
        name="Walking",
        description="Simple exercise for all fitness levels.",
        instructions="Warm up for 5 mins, walk briskly for 20-30 mins."
                     " Cool down.",
        benefits="Improves cardiovascular health, boosts mood, "
                 "aids in weight loss."
    ),
    Exercise(
        name="Yoga",
        description="Improve flexibility and reduce stress with yoga.",
        instructions="Basic poses: Mountain Pose, Downward Dog, Child's Pose. "
                     "Hold 20-30 secs.",
        benefits="Enhances flexibility, reduces stress, "
                 "improves mental well-being."
    ),
    Exercise(
        name="Water Aerobics",
        description="Low-impact exercise in water for cardio fitness.",
        instructions="Do leg lifts, arm circles, and jog in place in "
                     "waist-deep water for 30-45 mins.",
        benefits="Full-body workout with minimal joint impact, "
                 "improves strength."
    ),
    Exercise(
        name="Tai Chi",
        description="Gentle martial arts form that improves balance and reduces stress.",
        instructions="Guided Tai Chi routine with slow movements "
                     "and deep breathing for 20-30 mins.",
        benefits="Improves balance, reduces stress, enhances mental clarity."
    ),
    Exercise(
        name="Chair Yoga",
        description="Seated yoga to improve flexibility and strength.",
        instructions="Seated poses: Seated Forward Bend, Seated Twist."
                     " Hold 20-30 secs.",
        benefits="Increases flexibility and strength, "
                 "beneficial for limited mobility."
    ),
    Exercise(
        name="Resistance Band Exercises",
        description="Use resistance bands for strength without heavy weights.",
        instructions="Bicep curls, squats with resistance bands. "
                     "2-3 sets of 10-15 reps.",
        benefits="Builds muscle strength and endurance without heavy weights."
    ),
    Exercise(
        name="Balance Exercises",
        description="Improve balance and reduce fall risk.",
        instructions="Stand on one foot, heel-to-toe walk."
                     " Hold each position for 20-30 secs.",
        benefits="Enhances balance and coordination, reduces fall risk."
    ),
    Exercise(
        name="Pilates",
        description="Low-impact exercise focusing on core strength, flexibility, posture.",
        instructions="Guided Pilates routine with controlled movements "
                     "and breathing for 30-45 mins.",
        benefits="Improves core strength, flexibility, and posture."
    ),
    Exercise(
        name="Cycling",
        description="Stationary or outdoor biking for cardio health and leg strength.",
        instructions="Cycle at a moderate pace for 30-45 mins, "
                     "include warm-up and cool-down periods.",
        benefits="Boosts cardiovascular health, strengthens leg muscles."
    ),
    Exercise(
        name="Strength Training with Dumbbells",
        description="Use light weights to improve muscle strength and tone.",
        instructions="Dumbbell curls, shoulder presses."
                     " 2-3 sets of 10-15 reps.",
        benefits="Increases muscle strength and tone, enhances overall fitness."
    ),
    Exercise(
        name="Stretching",
        description="Simple stretches for flexibility and reduced muscle stiffness.",
        instructions="Hold each stretch for 20-30 secs, "
                     "focus on major muscle groups.",
        benefits="Improves flexibility, reduces muscle stiffness,"
                 " aids in recovery."
    ),
    Exercise(
        name="Dancing",
        description="Fun activity for cardio fitness and coordination.",
        instructions="Dance to favorite music for 30-45 mins, "
                     "include varied movements and styles.",
        benefits="Enhances cardiovascular fitness, coordination, and mood."
    )
]

exercise_actions = {exercise.name: exercise for exercise in exercises}

@router.get("/exercises/", response_model=List[str])
async def get_exercises():
    return [exercise.name for exercise in exercises]

@router.get("/exercises/{exercise_name}/details", response_model=Exercise)
async def get_exercise_details(exercise_name: str):
    exercise = exercise_actions.get(exercise_name)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise

@router.post("/custom-plan/", response_model=ExercisePlan)
async def create_custom_plan(user_profile: UserProfile):
    selected_exercises = []

    if user_profile.age >= 65:
        selected_exercises.extend([
            exercise_actions["Walking"],
            exercise_actions["Tai Chi"],
            exercise_actions["Chair Yoga"],
            exercise_actions["Balance Exercises"],
            exercise_actions["Stretching"]
        ])
    elif user_profile.weight / ((user_profile.height / 100) ** 2) >= 30:
        selected_exercises.extend([
            exercise_actions["Walking"],
            exercise_actions["Cycling"],
            exercise_actions["Water Aerobics"],
            exercise_actions["Dancing"],
            exercise_actions["Stretching"]
        ])

    if user_profile.special_health_conditions:
        if "arthritis" in user_profile.special_health_conditions:
            selected_exercises.extend([
                exercise_actions["Chair Yoga"],
                exercise_actions["Tai Chi"],
                exercise_actions["Water Aerobics"],
                exercise_actions["Stretching"]
            ])
        if "diabetes" in user_profile.special_health_conditions:
            selected_exercises.extend([
                exercise_actions["Walking"],
                exercise_actions["Cycling"],
                exercise_actions["Strength Training with Dumbbells"]
            ])

    selected_exercises = list({exercise.name: exercise for exercise in selected_exercises}.values())

    custom_plan = ExercisePlan(
        name="Custom Exercise Plan",
        description="A personalized exercise plan based on your profile.",
        exercises=selected_exercises,
        health_monitoring_integration=user_profile.health_monitoring_integration,
        progress_tracking=user_profile.progress_tracking
    )
    return custom_plan

app = FastAPI()
app.include_router(router)
