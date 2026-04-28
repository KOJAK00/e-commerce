from sqlalchemy.orm import Session
from fastapi import FastAPI,Depends,status,Response,HTTPException,APIRouter
from typing import List
import schemas,database,models,oauth2

router = APIRouter(prefix='/business',tags=["business"])

@router.post('', response_model=schemas.BusinessResponse)
def create_business(
    request: schemas.BusinessCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user) 
):
    new_business = models.Business(
        business_name=request.business_name,
        city=request.city,
        region=request.region,
        business_description=request.business_description,
        owner_id=current_user.id 
    )

    db.add(new_business)
    db.commit()
    db.refresh(new_business)

    return new_business