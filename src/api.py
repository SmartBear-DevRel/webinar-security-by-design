import os
from datetime import datetime, timezone, timedelta
from typing import Optional

from fastapi import FastAPI, HTTPException
from jose import jwt
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import sessionmaker

from src.models import BookListing, Order, User
from src.schemas import (
    PlaceOrder,
    GetOrderDetails,
    GetBookDetails,
    ListBook,
    Login,
    AccessToken,
    ListBooks,
    ListOrders,
    SellerProfile,
    UserProfile,
    UpdateUserProfile,
)

server = FastAPI(debug=True, title="E-commerce API")

db_uri = os.getenv("db_uri", None) or "postgresql+psycopg://postgres:postgres@localhost:5432/postgres"
session_maker = sessionmaker(bind=create_engine(db_uri))


def book_model_to_dict(book_model):
    book = {
        "id": book_model.id,
        "created": book_model.created,
        "last_updated": book_model.updated,
        "author": book_model.author,
        "title": book_model.title,
        "format": book_model.format,
        "description": book_model.description,
        "price": book_model.price,
        "percent_discount": book_model.percent_discount,
        "discount_min_loyalty_points": book_model.discount_min_loyalty_points,
    }
    if book_model.format == "printed":
        book["pages"] = book_model.pages
        book["price_per_page"] = book_model.price / book_model.pages
    elif book_model.format == "ebook":
        book["byte_size"] = book_model.byte_size
        book["price_per_byte"] = book_model.price / book_model.byte_size
    return book


def generate_token(user_id, hour_duration):
    now = datetime.now(timezone.utc)
    payload = {
        "iss": "https://auth.example.example",
        "sub": str(user_id),
        "aud": "https://ecommerce.example/api",
        "iat": now.timestamp(),
        "exp": (now + timedelta(hours=hour_duration)).timestamp(),
    }
    return jwt.encode(claims=payload, key="secret", algorithm="HS256")


@server.post("/login", response_model=AccessToken)
def login(login_details: Login):
    with session_maker() as session:
        user = session.execute(
            text(
                f"select * from user where username = '{login_details.username}' "
                f"and password = '{login_details.password}';"
            )
        ).fetchone()
        if user is None:
            raise HTTPException(status_code=401, detail=f"Wrong username or password")
        return {
            "access_token": generate_token(user_id=user.id, hour_duration=1),
            "refresh_token": generate_token(user_id=user.id, hour_duration=24),
        }


@server.get("/sellers/{seller_id}", response_model=SellerProfile)
def get_seller_details(seller_id: int):
    with session_maker() as session:
        seller = session.execute(
            text(f"select * from seller where id = '{seller_id}';")
        ).fetchone()
        if seller is None:
            raise HTTPException(
                status_code=404, detail=f"Seller with ID {seller_id} does not exist"
            )
        return {
            "id": seller.id,
            "created": seller.created,
            "last_updated": seller.updated,
            "name": seller.name,
            "address": seller.address,
            "sales": seller.sales,
            "account_details": seller.account_details,
        }


@server.put("/users/{user_id}", response_model=UserProfile)
def update_user_profile(user_id: int, user_details: UpdateUserProfile):
    with session_maker() as session:
        user = session.scalar(select(User).where(User.id == user_id))
        if user is None:
            raise HTTPException(
                status_code=404, detail=f"User with ID {user_id} does not exist"
            )
        for key, value in user_details:
            setattr(user, key, value)
        session.commit()
        return {
            "id": user.id,
            "created": user.created,
            "last_updated": user.updated,
            "name": user.name,
            "address": user.address,
            "avatar_url": user.avatar_url,
            "card_details": user.card_details,
            "loyalty_points": user.loyalty_points,
        }


@server.get("/books", response_model=ListBooks)
def list_books(
    offset: Optional[int] = 0, limit: Optional[int] = 10, filter: Optional[str] = ""
):
    with session_maker() as session:
        books = session.execute(
            text(
                f"select * from book_listing where discount_min_loyalty_points < 50 and "
                f"description like '%{filter}%' offset {offset} limit {limit};"
            )
        )
        return {"books": [book_model_to_dict(book) for book in books]}


@server.post("/books", response_model=GetBookDetails)
def create_book_listing(book_details: ListBook):
    # restrict access to seller scope
    with session_maker() as session:
        book = BookListing(
            seller_id=3,
            author=book_details.author,
            title=book_details.title,
            description=book_details.description,
            price=book_details.price,
            format=book_details.format,
            pages=book_details.pages,
            byte_size=book_details.byte_size,
        )
        session.add(book)
        session.commit()
        return book_model_to_dict(book)


@server.post("/admin/books", response_model=GetBookDetails)
def create_book_listing(book_details: ListBook):
    with session_maker() as session:
        book = BookListing(
            seller_id=3,
            author=book_details.author,
            title=book_details.title,
            description=book_details.description,
            price=book_details.price,
            format=book_details.format,
            pages=book_details.pages,
            byte_size=book_details.byte_size,
        )
        session.add(book)
        session.commit()
        return book_model_to_dict(book)


@server.get("/books/{book_id}", response_model=GetBookDetails)
def get_book_listing_details(book_id: int):
    with session_maker() as session:
        book = session.scalar(select(BookListing).where(BookListing.id == book_id))
        return book_model_to_dict(book)


@server.get("/orders", response_model=ListOrders)
def list_orders(
    offset: Optional[int] = 0,
    limit: Optional[int] = 10,
    status: Optional[str] = "delivered",
):
    with session_maker() as session:
        orders = session.execute(
            text(
                f"select * from order where user_id = 1 "
                f"and status = '{status} offset {offset} limit {limit}'"
            )
        )
        return [
            {
                "id": order.id,
                "created": order.created,
                "last_updated": order.updated,
                "books": order.books,
                "status": order.status,
                "delivery_address": order.delivery_address,
            }
            for order in orders
        ]


@server.put("/orders/{order_id}", response_model=GetOrderDetails)
def update_ride_details(order_id: int, order_details: PlaceOrder):
    with session_maker() as session:
        order = session.scalar(select(Order).where(Order.id == order_id))
        for key, value in order_details:
            setattr(order, key, value)
        session.commit()
        return {
            "id": order.id,
            "created": order.created,
            "last_updated": order.updated,
            "books": order.books,
            "status": order.status,
            "delivery_address": order.delivery_address,
        }
