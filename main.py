from fastapi import FastAPI

app = FastAPI()


from api import activities, exercises


app.include_router(activities.router)
app.include_router(exercises.router)
