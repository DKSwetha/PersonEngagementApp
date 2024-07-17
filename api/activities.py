from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter()


class Activity(BaseModel):
    name: str
    description: str


activities = [
    Activity(name="Crossword", description="Engage in a crossword puzzle to stimulate your brain."),
    Activity(name="Sudoku", description="Play Sudoku to challenge your logical thinking."),
    Activity(name="Jigsaw Puzzles", description="Solve jigsaw puzzles to enhance visual-spatial skills."),
    Activity(name="Memory Games", description="Play memory games to improve cognitive abilities."),
    Activity(name="Trivia Quizzes", description="Test general knowledge and memory recall with trivia quizzes."),
    Activity(name="Brain Teasers", description="Solve brain teasers to exercise your brain and think creatively."),
    Activity(name="Board Games", description="Enjoy board games like Scrabble, Chess, and Checkers for strategic thinking."),
    Activity(name="Painting or Drawing", description="Experience painting or drawing to enhance motor skills.")
]


@router.get("/activities/", response_model=List[Activity])
async def get_activities():
    return activities


activity_actions = {
    "Crossword": "Opening crossword puzzle application...",
    "Sudoku": "Opening Sudoku application...",
    "Jigsaw Puzzles": "Opening jigsaw puzzle application...",
    "Memory Games": "Opening memory game application...",
    "Trivia Quizzes": "Opening trivia quiz application...",
    "Brain Teasers": "Opening brain teaser application...",
    "Board Games": "Opening board game application...",
    "Painting or Drawing": "Opening painting or drawing application..."
}


@router.get("/activities/{activity_name}/start")
async def start_activity(activity_name: str):
    if activity_name not in activity_actions:
        raise HTTPException(status_code=404, detail="Activity not found")
    action_message = activity_actions[activity_name]
    return {"message": action_message}


from fastapi import FastAPI

app = FastAPI()
app.include_router(router)
