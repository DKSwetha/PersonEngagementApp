"""
This module defines an API for activities using FastAPI.
It includes endpoints to retrieve a list of activities
and to start a specific activity.
"""

from fastapi import APIRouter, HTTPException, FastAPI
from pydantic import BaseModel
from typing import List

router = APIRouter()

class Activity(BaseModel):
    name: str
    description: str

activities = [
    Activity(name="Crossword",
             description="Stimulate your brain with a crossword puzzle."),
    Activity(name="Sudoku",
             description="Challenge your logic with Sudoku."),
    Activity(name="Jigsaw Puzzles",
             description="Enhance visual-spatial skills with jigsaw puzzles."),
    Activity(name="Memory Games",
             description="Improve cognitive abilities with memory games."),
    Activity(name="Trivia Quizzes",
             description="Test your knowledge with trivia quizzes."),
    Activity(name="Brain Teasers",
             description="Exercise your brain with creative brain teasers."),
    Activity(name="Board Games",
             description="Enjoy strategic thinking with board games."),
    Activity(name="Painting or Drawing",
             description="Enhance motor skills with painting or drawing.")
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

app = FastAPI()
app.include_router(router)
