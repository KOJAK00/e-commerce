from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
import models,schemas,database,oauth2
from datetime import datetime
router = APIRouter(prefix="/bid", tags=["bid"])


@router.post("/bid/{auction_id}")
def place_bid(
    auction_id: int,
    amount: float,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    auction = db.query(models.Auction).join(models.Business).filter(
        models.Auction.id == auction_id,
        models.Business.owner_id != current_user.id,
        models.Auction.is_active == True
    ).first()

    if not auction:
        raise HTTPException(status_code=404, detail="Auction not found")
    if auction.end_time < datetime.utcnow():
       raise HTTPException(
          status_code=400,
          detail="Auction ended"
    )
    if amount <= auction.current_price:
        raise HTTPException(status_code=400, detail="Bid must be higher")

    auction.current_price = amount

    bid = models.Bid(
        auction_id=auction_id,
        user_id=current_user.id,
        amount=amount
    )

    db.add(bid)
    db.commit()

    return {"message": "Bid placed successfully"}