from sqlalchemy import Column, Integer, String, ForeignKey,Date,func,Text,Boolean,Numeric
from sqlalchemy.orm import relationship,DeclarativeBase
from datetime import date
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