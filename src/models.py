from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import MetaData, ForeignKey, DateTime, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s_idx",
            "uq": "uq_%(table_name)s_%(column_0_name)s_key",
            "ck": "ck_%(table_name)s_%(constraint_name)s_check",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s_fkey",
            "pk": "pk_%(table_name)s_pkey",
        }
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda _: datetime.now(timezone.utc)
    )
    updated: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda _: datetime.now(timezone.utc)
    )


class BookListing(Base):
    __tablename__ = "book_listing"

    seller_id: Mapped[int] = mapped_column(ForeignKey("seller.id"))
    title: Mapped[str]
    author: Mapped[str]
    description: Mapped[str]
    price: Mapped[float]
    percent_discount: Mapped[Optional[float]]
    discount_min_loyalty_points: Mapped[int] = mapped_column(default=0)
    format: Mapped[str]
    pages: Mapped[Optional[int]]
    byte_size: Mapped[Optional[int]]


class BookOrders(Base):
    __tablename__ = "book_orders"

    order_id: Mapped[int] = mapped_column(ForeignKey("customer_order.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("book_listing.id"))


class Order(Base):
    __tablename__ = "customer_order"

    user_id: Mapped[int]
    delivery_address: Mapped[str]
    status: Mapped[str]
    books: Mapped[List[BookOrders]] = relationship()


class Review(Base):
    __tablename__ = "review"

    book_id: Mapped[int] = mapped_column(ForeignKey("book_listing.id"))
    user_id: Mapped[int]
    rating: Mapped[int]
    review: Mapped[Optional[str]]
    upvotes: Mapped[int] = mapped_column(default=0)


class User(Base):
    __tablename__ = "user_profile"

    username: Mapped[str]
    password: Mapped[str]
    avatar: Mapped[Optional[str]]
    name: Mapped[str]
    address: Mapped[str]
    card_details: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(default=False)
    loyalty_points: Mapped[int] = mapped_column(default=0)


class Seller(Base):
    __tablename__ = "seller"

    name: Mapped[str]
    address: Mapped[str]
    account_details: Mapped[str]
    sales: Mapped[int]
    book_listings: Mapped[List[BookListing]] = relationship()
