from fastapi import Request,HTTPException,status,APIRouter,Depends
import models,database,schemas
from sqlalchemy.orm import Session
from hashing import hash
router = APIRouter(prefix='/user',tags=["users"])
@router.post('',response_model=schemas.UserResponse)
def create(request : schemas.user,db : Session = Depends(database.get_db)):
    existing = db.query(models.User).filter(
    models.User.username == request.username).first()
    if existing:
      raise HTTPException(
        status_code=400,
        detail="Username already exists")
    existing1 = db.query(models.User).filter(
    models.User.email == request.email).first()
    if existing1:
      raise HTTPException(
        status_code=400,
        detail="Email already exists")
    new_user = models.User(username = request.username,email = request.email,password=hash.argon2(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
