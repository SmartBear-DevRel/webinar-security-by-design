from typing import Optional

from fastapi import FastAPI
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import sessionmaker

from models import BookListing, Order
from schemas import PlaceOrder, GetOrderDetails, GetBookDetails, ListBook, Login, AccessToken, ListBooks, ListOrders, \
    SellerProfile, CustomerProfile, UpdateCustomerProfile

server = FastAPI(debug=True, title="E-commerce API")

session_maker = sessionmaker(
    bind=create_engine("postgresql+psycopg://postgres:postgres@localhost:5432")
)


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


@server.post("/login", response_model=AccessToken)
def login(login_details: Login):
    pass


@server.get("/sellers/{seller_id}", response_model=SellerProfile)
def get_seller_details(seller_id: int):
    pass


@server.put("/users/{user_id}", response_model=CustomerProfile)
def update_user_profile(user_id: int, user_details: UpdateCustomerProfile):
    pass


@server.get("/books", response_model=ListBooks)
def list_books(offset: Optional[int] = 0, limit: Optional[int] = 10, filter: Optional[str] = ""):
    with session_maker() as session:
        # rides = session.scalars(
        #     select(Ride).where(
        #         Ride.customer_id == "customer_1",
        #         Ride.status == status
        #     )
        # )
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
def list_orders(offset: Optional[int] = 0, limit: Optional[int] = 10, status: Optional[str] = "delivered"):
    with session_maker() as session:
        # orders = session.scalars(
        #     select(Order).where(
        #         Ride.customer_id == "customer_1",
        #         Ride.status == status
        #     )
        # )
        orders = session.execute(
            text(
                f"select * from order where customer_id = 'customer_1' "
                f"and status = '{status} offset {offset} limit {limit}'"
            )
        )
        # orders = session.execute(
        #     text(f"select * from order where customer_id = 'customer_1' offset {offset} limit {limit}")
        # )
        return [{
            "id": order.id,
            "created": order.created,
            "last_updated": order.updated,
            "books": order.books,
            "status": order.status,
            "delivery_address": order.delivery_address
        } for order in orders]


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
            "delivery_address": order.delivery_address
        }




# @server.get("/cars/{ids}")
# def integer_ids_cars():
#     # ride-sharing app, we explore existing vehicles playing with IDs
#     pass
#
#
# @server.post("/cart")
# def create_cart():
#     # we add items to cart
#     pass
#
#
# @server.put("/cart/{id}")
# def mass_assignment_attack():
#     # we set status to paid
#     pass
#
#
# @server.get("/users/{id}")
# def get_user_details():
#     # we see user_type property
#     pass
#
#
# @server.put("/users/{id}")
# def another_mass_assignment_attack():
#     # we set user_type to admin; the property isn't exposed in the PUT schema,
#     #   but because we allow unknown properties, the attack succeeds
#     pass
#
#
# @server.get("/ride/{id}")
# def too_many_ids():
#     # we return details of the ride, including driver ID, vehicle ID, and such
#     pass
#
#
# @server.get("/catalogue")
# def improper_pagination():
#     # lack of default pagination returns everything (improper pagination)
#     # lack of value constrains allows users to set 1m items per page (unbound integers)
#     # unrestricted string filter allows injection attack, use "' OR 1=1 --" strategy or similar;
#     #   if we have "deleted" items marked with a flag, they'd show up
#     pass
#
#
# @server.post("/books")
# def problematic_flexible_schemas():
#     # ebook and printed book models combined with optional params
#     # shared model also in db with optional columns
#     # break response in below listing endpoint because models aren't right
#     pass
#
#
# @server.get("/printed-books")
# def list_printed_books():
#     pass
#
#
# @server.post("/stock")
# def weak_implicit_rbac():
#     # level 1 can read, level 2 can read and write
#     # us can see canada stock and canada can see us stock
#     # by mistake, we only check country belonging and bypass the hierarchy level
#     pass
#
#
# @server.get("/admin/users/{id}")
# def weak_endpoint_specific_admin():
#     # we can retrieve details of all users and also make modifications
#     pass
#
#
# @server.post("/orders/{id}")
# def cluttered_endpoint():
#     # if payment details in payload, it's payment
#     # if user account and action=refund, we know it's a refund request
#     # if action=cancel, we know it's cancellation
#     pass
