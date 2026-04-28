from fastapi import FastAPI
import models
from database import engine
from fastapi.staticfiles import StaticFiles
from routers import user,business,login,products,auction,bid

app=FastAPI()

models.Base.metadata.create_all(engine)
app.include_router(login.router)
app.include_router(user.router)
app.include_router(business.router)
app.include_router(products.router)
app.include_router(auction.router)
app.include_router(bid.router)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
