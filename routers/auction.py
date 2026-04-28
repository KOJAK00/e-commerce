from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
import models,schemas,database,oauth2
from datetime import datetime,timezone
router = APIRouter(prefix="/auction", tags=["auction"])
@router.post("")
def create_auction(
    request: schemas.AuctionCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    product = db.query(models.Product).join(models.Business).filter(
    models.Product.id == request.product_id,
    models.Business.owner_id == current_user.id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if request.end_time <= datetime.now(timezone.utc):
        raise HTTPException(
          status_code=400,
          detail="End time must be in the future"
    )
    auction = models.Auction(
        business_id = product.business_id,
        product_id = request.product_id,
        start_price=request.start_price,
        current_price=request.start_price,
        end_time=request.end_time
    )

    db.add(auction)
    db.commit()
    db.refresh(auction)

    return auction