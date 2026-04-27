from fastapi import FastAPI
import models
from database import engine

# from .routers import login,blog,user

app=FastAPI()

models.Base.metadata.create_all(engine)

@app.get('/')
def index():
    return 'Hi'