from fastapi import Request,HTTPException,status,APIRouter,Depends
import models,database,schemas
from sqlalchemy.orm import Session
from hashing import hash
router = APIRouter(prefix='/user',tags=["users"])
@router.post('',response_model=schemas.UserResponse)
def create(request : schemas.user,db : Session = Depends(database.get_db)):
    new_user = models.User(username = request.username,email = request.email,password=hash.argon2(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user