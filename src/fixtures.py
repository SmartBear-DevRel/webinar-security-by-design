import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import BookListing, Seller, User

db_uri = (
    os.getenv("db_uri", None)
    or "postgresql+psycopg://postgres:postgres@localhost:5432/postgres"
)
session_maker = sessionmaker(bind=create_engine(db_uri))

with session_maker() as session:
    user = User(
        username="username",
        password="egg",
        name="User Name",
        address="Some address",
        card_details="3456765456",
    )
    seller = Seller(
        name="Seller",
        address="Some address",
        account_details="3456765456",
        sales=355,
    )
    session.add_all([seller, user])
    session.commit()
    book1 = BookListing(
        seller_id=seller.id,
        title="Microservice APIs",
        author="Jose Haro Peralta",
        description="A book about microservice APIs",
        format="printed",
        pages=440,
        price=55,
    )
    book2 = BookListing(
        seller_id=seller.id,
        title="Microservice APIs",
        author="Jose Haro Peralta",
        description="A book about microservice APIs",
        format="ebook",
        byte_size=550,
        price=30,
        percent_discount=40,
        discount_min_loyalty_points=1000,
    )
    book3 = BookListing(
        seller_id=seller.id,
        title="Microservices Patterns",
        author="Chris Richardson",
        description="A book about microservices patterns",
        format="printed",
        pages=550,
        price=60,
        percent_discount=20,
        discount_min_loyalty_points=500,
    )
    session.add_all([book1, book2, book3])
    session.commit()
