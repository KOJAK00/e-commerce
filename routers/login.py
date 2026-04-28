from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
import schemas,database,models,tokens
from sqlalchemy.orm import Session
from hashing import hash
router  = APIRouter(tags=['login'])

@router.post('/login')

def login(request : OAuth2PasswordRequestForm = Depends(),db : Session = Depends(database.get_db)):
    
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"invalid credentials")
    if not hash.verify(user.password,request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"invalid credentials")
    access_token = tokens.create_access_token(data={"sub": user.username})
    return {"access_token" : access_token, "token_type" : "bearer"}
