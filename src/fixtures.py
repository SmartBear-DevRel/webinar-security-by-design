from datetime import datetime, timezone

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import BookListing, Seller

session_maker = sessionmaker(bind=create_engine("postgresql+psycopg://postgres:postgres@localhost:5432"))

with session_maker() as session:
    seller = Seller(
        name="Seller",
        address="Some address",
        account_details="3456765456",
        sales=355,
    )
    session.add(seller)
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
