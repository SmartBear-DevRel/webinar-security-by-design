import enum
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, field_validator, constr


class Login(BaseModel):
    username: constr(min_length=5)
    password: constr(min_length=5)


class AccessToken(BaseModel):
    access_token: constr(min_length=5)
    refresh_token: constr(min_length=5)


class OrderStatusEnum(str, enum.Enum):
    placed = "placed"
    paid = "paid"
    delivered = "delivered"


class MakePayment(BaseModel):
    card_number: constr(min_length=5)
    cvv: int


class GetPayment(MakePayment):
    id: int
    created: datetime
    last_updated: datetime


class PlaceOrder(BaseModel, extra=Extra.forbid):
    books: list[int]
    delivery_address: constr(min_length=5)

    @field_validator("delivery_address")
    def delivery_address_non_null(cls, value: str):
        assert "\u0000" not in value, "delivery_address cannot contain NUL (0x00) bytes."
        if value.isdigit():
            assert int(value) != 0, "delivery_address cannot have null-like values."


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
    seller_id: Optional[int]
    format: BookFormatEnum
    author: constr(min_length=5)
    title: constr(min_length=5)
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
    name: constr(min_length=5)
    address: constr(min_length=5)
    sales: int
    account_details: constr(min_length=5)


class UpdateUserProfile(BaseModel, extra=Extra.forbid):
    name: constr(min_length=5)
    avatar_url: Optional[str] = None
    address: constr(min_length=5)
    card_details: constr(min_length=5)
    loyalty_points: int


class UserProfile(UpdateUserProfile):
    id: int
    created: datetime
    last_updated: datetime
