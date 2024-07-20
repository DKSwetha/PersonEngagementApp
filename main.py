from fastapi import FastAPI
from api import activities, exercises
app = FastAPI()

app.include_router(activities.router)
app.include_router(exercises.router)
