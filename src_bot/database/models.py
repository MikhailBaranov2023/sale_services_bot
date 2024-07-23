from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Text, Float, Boolean, DateTime, func, Integer, BigInteger, ForeignKey, Column


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_name: Mapped[str] = mapped_column(unique=True, nullable=True, default='нет username')
    chat_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    spam: Mapped[bool] = mapped_column(default=False)
    blocked: Mapped[bool] = mapped_column(default=False)


class Product(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    image: Mapped[int] = mapped_column(BigInteger, nullable=True)
    price: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)


class Order(Base):
    __tablename__ = 'order'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    amount: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=True)
    payment_status: Mapped[bool] = mapped_column(Boolean, default=False)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)


class OrderShop(Base):
    __tablename__ = 'order_shop'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    url: Mapped[str] = mapped_column(Text, nullable=True)
    description: Mapped[str] = mapped_column(Text)
    address: Mapped[str] = mapped_column(String(200), nullable=True)
    amount: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=True)
    payment_status: Mapped[bool] = mapped_column(Boolean, default=False)
    order_status: Mapped[bool] = mapped_column(Boolean, default=False)
    track_number: Mapped[str] = mapped_column(String(50), nullable=True)
    cancel_status: Mapped[bool] = mapped_column(Boolean, default=False)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
