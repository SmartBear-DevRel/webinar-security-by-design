import enum
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra


class Login(BaseModel):
    username: str
    password: str


class AccessToken(BaseModel):
    access_token: str
    refresh_token: str


class OrderStatusEnum(str, enum.Enum):
    booked = "placed"
    paid = "paid"
    completed = "delivered"


class MakePayment(BaseModel):
    card_number: str
    cvv: int


class GetPayment(MakePayment):
    id: int
    created: datetime
    last_updated: datetime


class PlaceOrder(BaseModel, extra=Extra.allow):
    books: list[int]
    delivery_address: str


class GetOrderDetails(PlaceOrder):
    id: int
    created: datetime
    last_updated: datetime
    status: OrderStatusEnum


class ListOrders(BaseModel):
    orders: list[GetOrderDetails]


class BookFormatEnum(str, enum.Enum):
    printed = "printed"
    ebook = "ebook"


class ListBook(BaseModel):
    format: BookFormatEnum
    author: str
    title: str
    description: Optional[str]
    price: float
    percent_discount: Optional[float] = None
    discount_min_loyalty_points: Optional[int] = None
    pages: Optional[int] = None
    byte_size: Optional[int] = None


class GetBookDetails(ListBook):
    id: int
    created: datetime
    last_updated: datetime
    price_per_page: Optional[float] = None
    price_per_byte: Optional[float] = None


class ListBooks(BaseModel):
    books: list[GetBookDetails]


class SellerProfile(BaseModel):
    id: int
    created: datetime
    last_updated: datetime
    name: str
    address: str
    sales: int
    account_details: str



class UpdateCustomerProfile(BaseModel):
    name: str
    avatar_url: Optional[str] = None
    address: str
    card_details: str
    loyalty_points: int


class CustomerProfile(BaseModel):
    id: str
    created: datetime
    last_updated: datetime
