from sqlalchemy.orm import Session
from fastapi import FastAPI,Depends,status,Response,HTTPException,APIRouter,UploadFile, File
from utils.file_upload import save_file
from typing import List
import schemas,database,models,oauth2

router = APIRouter(prefix='/business',tags=["business"])

@router.post('')
def create_business(
    request: schemas.BusinessCreate =Depends(),logo: UploadFile = File(None),
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user) 
):
    existing = db.query(models.Business).filter(
    models.Business.business_name == request.business_name).first()
    if existing:
      raise HTTPException(
        status_code=400,
        detail="Business name already exists")
    logo_path = "uploads/logos/default.jpg"

    if logo:
      logo_path = save_file(logo, "logos")
    new_business = models.Business(
            
            **request.model_dump(),
            owner_id=current_user.id,
            logo=logo_path
        )
    db.add(new_business)
    db.commit()
    db.refresh(new_business)

    return new_business

@router.get('', response_model=list[schemas.BusinessResponse])
def get_businesses(db : Session = Depends(database.get_db),current_user: models.User = Depends(oauth2.get_current_user)):
   businesses = db.query(models.Business).filter(models.Business.owner_id==current_user.id).all()
   return businesses

@router.put('',response_model=schemas.BusinessResponse)
def update_business(id : int,request: schemas.BusinessCreate,db: Session = Depends(database.get_db),current_user: models.User = Depends(oauth2.get_current_user)):
   business = db.query(models.Business).filter(models.Business.id == id , models.Business.owner_id == current_user.id)
   if not business.first():
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"business with the id {id} is not available")
   existing = db.query(models.Business).filter(
    models.Business.business_name == request.business_name,
    models.Business.id != id).first()
   if existing:
      raise HTTPException(
        status_code=400,
        detail="Business name already exists")
   
   data = request.model_dump(exclude_unset=True)

   if "logo" in data and not data["logo"]:
      data ["logo"] = "default.jpg"

   business.update(data, synchronize_session=False)
   db.commit()
   return business.first()