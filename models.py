from sqlalchemy import Column, Integer, String, ForeignKey,Date,func,Text,Boolean,Numeric,Float,DateTime
from sqlalchemy.orm import relationship,DeclarativeBase
from datetime import date,datetime
from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True,index=True)  
    username = Column(String(20),unique=True,nullable=False)  
    email = Column(String(200),unique=True,nullable=False)
    password = Column(String(100),nullable=False)
    is_verified = Column(Boolean,default=False)
    join_date = Column(Date,default=date.today,nullable=False)
    businesses = relationship("Business", back_populates="owner")

class Business(Base):
    __tablename__ = 'businesses'
    id = Column(Integer,primary_key=True,index=True) 
    business_name = Column(String(100),unique=True,nullable=False)  
    city = Column(String(200),default="Unspecified",nullable=False)
    region = Column(String(200),default="Unspecified",nullable=False)
    business_description = Column(Text,nullable=True)
    logo = Column(String(200),nullable=False,default="default.jpg")
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="businesses")
    products = relationship("Product", back_populates="business")

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(100),nullable=False,index=True) 
    category = Column(String(30),index=True) 
    original_price = Column(Numeric(12, 2))
    new_price = Column(Numeric(12, 2))
    percentage_discount =Column(Integer)
    offer_expiration_date = Column(Date,default=date.today)
    product_image = Column(String(200),nullable=False,default="product_default.jpg")
    business_id = Column(Integer,ForeignKey("businesses.id"), nullable=False)
    business = relationship("Business", back_populates="products")

class Auction(Base):
    __tablename__ = "auctions"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    
    start_price = Column(Float)
    current_price = Column(Float, default=0)
    end_time = Column(DateTime)

    is_active = Column(Boolean, default=True)
    business_id = Column(Integer,ForeignKey("businesses.id"), nullable=False)
    product = relationship("Product")
    business = relationship("Business")

class Bid(Base):
    __tablename__ = "bids"

    id = Column(Integer, primary_key=True)
    auction_id = Column(Integer, ForeignKey("auctions.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    amount = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    