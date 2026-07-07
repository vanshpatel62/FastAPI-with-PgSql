"""
schemas.py
----------
"Schemas" are NOT database tables. They are shapes/rules that FastAPI uses to:
  1. Check incoming data from the user is valid (before we insert it in DB)
  2. Format the data we send back as a response

For each table we usually make TWO schemas:
  - "...Create"  -> fields the USER sends us (no auto-generated fields like id, dates)
  - the "full" one -> everything, including auto fields, used for the RESPONSE

This keeps auto-generated columns (like cust_id, join_date) safely controlled by
the database only, not by whatever the user types.
"""

from pydantic import BaseModel, EmailStr   # BaseModel = base class for all schemas, EmailStr = validates a proper email format
from datetime import datetime
from typing import Optional
from decimal import Decimal                # used for money fields (numeric in Postgres) - safer than float for prices


# ==================== CUSTOMERS ====================

class CustomerCreate(BaseModel):
    name: str
    email: EmailStr                      # automatically checks it looks like a real email, matching your CHECK constraint
    city: Optional[str] = None           # Optional + default None = this field is allowed to be skipped (your "city" column has no NOT NULL)

class Customer(CustomerCreate):          # inherits name, email, city from CustomerCreate, then adds DB-generated fields
    cust_id: int
    join_date: datetime

    class Config:
        from_attributes = True           # allows this schema to read values from DB row objects, not only plain dict


# ==================== PRODUCTS ====================

class ProductCreate(BaseModel):
    p_name: str
    category: Optional[str] = None
    price: Decimal
    stock: int
    brand: Optional[str] = None

class Product(ProductCreate):
    p_id: int

    class Config:
        from_attributes = True


# ==================== ORDERS ====================

class OrderCreate(BaseModel):
    cust_id: int
    status: str          # your table only allows: 'Pending', 'Shipped', 'Delivered', 'Cancelled'
                          # Postgres CHECK constraint already blocks bad values, so we don't have to repeat that rule here.
                          # OPTIONAL UPGRADE (not required now): use Python's `Enum` type here to also validate it before hitting the DB.
    total_amount: Decimal

class Order(OrderCreate):
    order_id: int
    order_date: datetime

    class Config:
        from_attributes = True


# ==================== ORDER ITEMS ====================
# NOTE: this table has NO single "id" column - its primary key is (order_id + items_id) together.

class OrderItemCreate(BaseModel):
    order_id: int
    items_id: int
    quantity: int
    unit_price: Decimal

class OrderItem(OrderItemCreate):
    class Config:
        from_attributes = True


# ==================== PAYMENTS ====================

class PaymentCreate(BaseModel):
    transaction_id: str
    order_id: int
    amount: Decimal
    payment_method: str      # 'Card', 'UPI', 'Cash'
    payment_status: str      # 'Successfully', 'Pending', 'Cancelled'

class Payment(PaymentCreate):
    payment_id: int
    payment_date: datetime

    class Config:
        from_attributes = True
