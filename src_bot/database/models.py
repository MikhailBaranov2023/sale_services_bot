from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, Text, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, nullable=True)
    username = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False, unique=True)
    referral_code = Column(String, nullable=True)


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    image = Column(String, nullable=False)


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type_order = Column(String(50), nullable=False)
    product = Column(Integer, ForeignKey('products.id'))
    description = Column(Text, nullable=True)
    order_amount = Column(Integer, nullable=True)
    order_status = Column(String(50), nullable=False, default='в обработке')
    date = Column(Date, nullable=False, default=func.now)
    user = Column(Integer, ForeignKey('users.id'))


class OrderShop(Base):
    __tablename__ = 'order_shop'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_urls = Column(String(500), nullable=False)
    address = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    # order_amount = Column(Integer, nullable=True)
    payment_status = Column(Boolean, default=False)
    order_status = Column(String(255), nullable=False, default='в обработке')
    # date = Column(Date, nullable=False, default=func.now)
    # track_number = Column(String(500), nullable=True)
    # user = Column(Integer, ForeignKey('users.id'))
    # username = Column(String, nullable=False)
