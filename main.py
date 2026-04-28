from fastapi import FastAPI
import models
from database import engine

from routers import user,business,login,products

app=FastAPI()

models.Base.metadata.create_all(engine)
app.include_router(login.router)
app.include_router(user.router)
app.include_router(business.router)
app.include_router(products.router)

