from fastapi import APIRouter,Depends,HTTPException,UploadFile,File
from sqlalchemy.orm import Session
from utils.file_upload import save_file
import models,schemas,database,oauth2
router = APIRouter(prefix="/products", tags=["products"])
@router.post('', response_model=schemas.ProductResponse)

def create_product(business_id: int,request: schemas.ProductCreate =Depends(),product_image: UploadFile =File(None),db: Session = Depends(database.get_db),current_user: models.User = Depends(oauth2.get_current_user)):
    business = db.query(models.Business).filter(
        models.Business.id == business_id,
        models.Business.owner_id == current_user.id
    ).first()

    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    image_path = "uploads/products/default.jpg"

    if product_image:
      image_path = save_file(product_image, "products")
    new_product = models.Product(
            **request.model_dump(),
            product_image=image_path,
            business_id=business_id)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.get('', response_model=list[schemas.ProductResponse])
def get_products(business_id: int,db: Session = Depends(database.get_db)):
    products = db.query(models.Product).filter(models.Product.business_id == business_id).all()

    return products

@router.put('/{id}', response_model=schemas.ProductResponse)
def update_product(
    id: int,
    request: schemas.ProductCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):

    product = db.query(models.Product).join(models.Business).filter(
        models.Product.id == id,
        models.Business.owner_id == current_user.id
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    data = request.model_dump(exclude_unset=True,exclude={"id","business_id"})

    if "product_image" in data and not data["product_image"]:
        data["product_image"] = "product_default.jpg"

    for key, value in data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)

    return product

@router.delete("/{id}")
def delete_product(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):

    product = db.query(models.Product).join(models.Business).filter(
        models.Product.id == id,
        models.Business.owner_id == current_user.id
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()

    return {"message": "Product deleted"}
