"""
routers/orders.py
------------------
CRUD endpoints for the "orders" table.
NOTE: this table has a foreign key (cust_id) pointing to customers.
Postgres itself will reject an insert/update if you give a cust_id that
doesn't exist - we don't need to check that manually in Python.
"""

from fastapi import APIRouter, Depends, HTTPException
from psycopg2.extensions import connection
from psycopg2 import errors               # lets us catch a specific Postgres error type (foreign key violation)
from database import get_db
from schemas import OrderCreate, Order

router = APIRouter(prefix="/orders", tags=["Orders"])


# ---------- CREATE ----------
@router.post("/", response_model=Order)
def create_order(order: OrderCreate, db: connection = Depends(get_db)):
    cursor = db.cursor()
    query = """
        INSERT INTO orders (cust_id, status, total_amount)
        VALUES (%s, %s, %s)
        RETURNING *;
    """
    try:
        cursor.execute(query, (order.cust_id, order.status, order.total_amount))
        new_order = cursor.fetchone()
        db.commit()
    except errors.ForeignKeyViolation:
        # OPTIONAL block: gives a friendly error instead of a raw database crash
        # when someone sends a cust_id that doesn't exist in customers table.
        db.rollback()
        raise HTTPException(status_code=400, detail="cust_id does not exist in customers table")
    finally:
        cursor.close()
    return new_order


# ---------- READ ALL ----------
@router.get("/", response_model=list[Order])
def get_orders(db: connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM orders ORDER BY order_id;")
    orders = cursor.fetchall()
    cursor.close()
    return orders


# ---------- READ ONE ----------
@router.get("/{order_id}", response_model=Order)
def get_order(order_id: int, db: connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM orders WHERE order_id = %s;", (order_id,))
    order = cursor.fetchone()
    cursor.close()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


# ---------- UPDATE ----------
@router.put("/{order_id}", response_model=Order)
def update_order(order_id: int, order: OrderCreate, db: connection = Depends(get_db)):
    cursor = db.cursor()
    query = """
        UPDATE orders
        SET cust_id = %s, status = %s, total_amount = %s
        WHERE order_id = %s
        RETURNING *;
    """
    cursor.execute(query, (order.cust_id, order.status, order.total_amount, order_id))
    updated_order = cursor.fetchone()
    db.commit()
    cursor.close()
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order


# ---------- DELETE ----------
@router.delete("/{order_id}")
def delete_order(order_id: int, db: connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM orders WHERE order_id = %s RETURNING order_id;", (order_id,))
    deleted = cursor.fetchone()
    db.commit()
    cursor.close()
    if not deleted:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": f"Order {order_id} deleted successfully"}
