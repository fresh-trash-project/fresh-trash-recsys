import enum
from typing import List
from sqlalchemy import Column, ForeignKey, Integer, String, Enum, JSON, DateTime, DOUBLE, BLOB, func
from sqlalchemy.orm import relationship, mapped_column, Mapped

from database import Base


class BaseModel:
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=True)
    modified_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)


"""
Member
"""
class LoginType(enum.Enum):
    EMAIL = "EMAIL"
    OAUTH = "OAUTH"

class UserRole(enum.Enum):
    USER = "ROLE_USER"
    BLACK_USER = "ROLE_BLACK_USER"
    ADMIN = "ROLE_ADMIN"
    ANONYMOUS = "ROLE_ANONYMOUS"

class AccountStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class Member(Base, BaseModel):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True)  

    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    rating = Column(DOUBLE, nullable=False)
    nickname = Column(String, unique=True, nullable=False)
    address = Column(JSON, nullable=False)
    file_name = Column(String, nullable=False)
    flag_count = Column(Integer, nullable=False)

    login_type = Column(Enum(LoginType), nullable=False)
    user_role = Column(Enum(UserRole), nullable=False)
    account_status = Column(Enum(AccountStatus), nullable=False)

    products: Mapped[List["Product"]] = relationship(back_populates="member")
    member_puchase_profile: Mapped["MemberPurchaseProfile"] = relationship(uselist=False, back_populates="member")


class MemberPurchaseProfile(Base, BaseModel):
    __tablename__ = "member_purchase_profiles"

    id = Column(Integer, primary_key=True)  

    product_cumulative_sum = Column(BLOB, nullable=True)
    purchase_count = Column(Integer, nullable=False, default=0)

    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"), unique=True, nullable=False)
    member: Mapped["Member"] = relationship("Member", back_populates="member_puchase_profile")


"""
Product
"""
class ProductCategory(enum.Enum):
    ELECTRONICS = 0
    CLOTHING = 1
    HOME_KITCHEN = 2
    BEAUTY = 3
    HEALTH = 4
    SPORTS = 5
    BOOKS = 6
    TOYS_GAMES = 7
    FURNITURE_DECOR = 8
    PET_SUPPLIES = 9
    PLANT_SUPPLIES = 10

class ProductStatus(enum.Enum):
    BEST = "BEST"
    GOOD = "GOOD"
    NORMAL = "NORMAL"
    WORST = "WORST"

class ProductSellStatus(enum.Enum):
    ONGOING = "ONGOING"
    BOOKING = "BOOKING"
    CLOSE = "CLOSE"

class Product(Base, BaseModel):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)

    product_price = Column(Integer, nullable=False)
    like_count = Column(Integer, nullable=False)
    view_count = Column(Integer, nullable=False)
    file_name = Column(String, nullable=False)
    
    product_category = Column(Enum(ProductCategory), nullable=False)
    product_status = Column(Enum(ProductStatus), nullable=False)
    sell_status = Column(Enum(ProductSellStatus), nullable=False)

    address = Column(JSON, nullable=False)
    product_deal_at = Column(DateTime(timezone=True), nullable=True)

    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"))
    member: Mapped["Member"] = relationship(back_populates="products")
    product_profile: Mapped["ProductProfile"] = relationship(uselist=False, back_populates="product")

class ProductProfile(Base, BaseModel):
    __tablename__ = "product_profiles"

    id = Column(Integer, primary_key=True)
    profile = Column(BLOB, nullable=True)

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), unique=True, nullable=False)
    product: Mapped["Product"] = relationship(back_populates="product_profile")
