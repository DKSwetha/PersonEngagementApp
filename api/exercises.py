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
        description="A simple exercise for all fitness levels.",
        instructions="Start with a warm-up walk for 5 minutes. Then walk at a brisk pace for 20-30 minutes. Cool down with a slow walk for 5 minutes.",
        benefits="Improves cardiovascular health, boosts mood, and aids in weight loss."
    ),
    Exercise(
        name="Yoga",
        description="Improve flexibility and reduce stress with yoga poses.",
        instructions="Start with basic poses like Mountain Pose, Downward Dog, and Child's Pose. Hold each pose for 20-30 seconds.",
        benefits="Enhances flexibility, reduces stress, and improves mental well-being."
    ),
    Exercise(
        name="Water Aerobics",
        description="Low-impact exercise in water to improve cardiovascular fitness.",
        instructions="Perform exercises like leg lifts, arm circles, and jogging in place in waist-deep water for 30-45 minutes.",
        benefits="Provides a full-body workout with minimal impact on joints, improving strength and endurance."
    ),
    Exercise(
        name="Tai Chi",
        description="A gentle form of martial arts that improves balance and reduces stress.",
        instructions="Follow a guided Tai Chi routine, focusing on slow, deliberate movements and deep breathing for 20-30 minutes.",
        benefits="Improves balance, reduces stress, and enhances overall mental clarity."
    ),
    Exercise(
        name="Chair Yoga",
        description="Yoga poses modified to be done while seated to improve flexibility and strength.",
        instructions="Perform seated poses like Seated Forward Bend and Seated Twist. Hold each pose for 20-30 seconds.",
        benefits="Increases flexibility and strength, especially beneficial for those with limited mobility."
    ),
    Exercise(
        name="Resistance Band Exercises",
        description="Using resistance bands to improve strength without heavy weights.",
        instructions="Perform exercises like bicep curls and squats using resistance bands. Do 2-3 sets of 10-15 repetitions.",
        benefits="Builds muscle strength and endurance without the need for heavy weights."
    ),
    Exercise(
        name="Balance Exercises",
        description="Exercises to improve balance and reduce the risk of falls.",
        instructions="Perform exercises like standing on one foot and heel-to-toe walk. Hold each position for 20-30 seconds.",
        benefits="Enhances balance and coordination, reducing the risk of falls."
    ),
    Exercise(
        name="Pilates",
        description="Low-impact exercise focusing on core strength, flexibility, and posture.",
        instructions="Follow a guided Pilates routine, focusing on controlled movements and breathing for 30-45 minutes.",
        benefits="Improves core strength, flexibility, and posture."
    ),
    Exercise(
        name="Cycling",
        description="Stationary or outdoor biking to improve cardiovascular health and leg strength.",
        instructions="Cycle at a moderate pace for 30-45 minutes, including a warm-up and cool-down period.",
        benefits="Boosts cardiovascular health and strengthens leg muscles."
    ),
    Exercise(
        name="Strength Training with Dumbbells",
        description="Using light weights to improve muscle strength and tone.",
        instructions="Perform exercises like dumbbell curls and shoulder presses. Do 2-3 sets of 10-15 repetitions.",
        benefits="Increases muscle strength and tone, enhancing overall fitness."
    ),
    Exercise(
        name="Stretching",
        description="Simple stretches to improve flexibility and reduce muscle stiffness.",
        instructions="Hold each stretch for 20-30 seconds, focusing on major muscle groups like hamstrings, quadriceps, and shoulders.",
        benefits="Improves flexibility and reduces muscle stiffness, aiding in recovery and preventing injuries."
    ),
    Exercise(
        name="Dancing",
        description="Fun and social activity that improves cardiovascular fitness and coordination.",
        instructions="Dance to your favorite music for 30-45 minutes, incorporating a variety of movements and styles.",
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
