"""
routers/order_items.py
-----------------------
CRUD endpoints for "order_items" table.
IMPORTANT DIFFERENCE: this table has NO single auto-id column.
Its primary key is TWO columns together: (order_id, items_id).
So to read/update/delete ONE row, we need BOTH values in the URL.
"""

from fastapi import APIRouter, Depends, HTTPException
from psycopg2.extensions import connection
from database import get_db
from schemas import OrderItemCreate, OrderItem

router = APIRouter(prefix="/order-items", tags=["Order Items"])


# ---------- CREATE ----------
@router.post("/", response_model=OrderItem)
def create_order_item(item: OrderItemCreate, db: connection = Depends(get_db)):
    cursor = db.cursor()
    query = """
        INSERT INTO order_items (order_id, items_id, quantity, unit_price)
        VALUES (%s, %s, %s, %s)
        RETURNING *;
    """
    cursor.execute(query, (item.order_id, item.items_id, item.quantity, item.unit_price))
    new_item = cursor.fetchone()
    db.commit()
    cursor.close()
    return new_item


# ---------- READ ALL ----------
@router.get("/", response_model=list[OrderItem])
def get_order_items(db: connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM order_items;")
    items = cursor.fetchall()
    cursor.close()
    return items


# ---------- READ ONE (needs both order_id AND items_id) ----------
@router.get("/{order_id}/{items_id}", response_model=OrderItem)
def get_order_item(order_id: int, items_id: int, db: connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM order_items WHERE order_id = %s AND items_id = %s;",
        (order_id, items_id)
    )
    item = cursor.fetchone()
    cursor.close()
    if not item:
        raise HTTPException(status_code=404, detail="Order item not found")
    return item


# ---------- UPDATE ----------
@router.put("/{order_id}/{items_id}", response_model=OrderItem)
def update_order_item(order_id: int, items_id: int, item: OrderItemCreate, db: connection = Depends(get_db)):
    cursor = db.cursor()
    query = """
        UPDATE order_items
        SET quantity = %s, unit_price = %s
        WHERE order_id = %s AND items_id = %s
        RETURNING *;
    """
    cursor.execute(query, (item.quantity, item.unit_price, order_id, items_id))
    updated_item = cursor.fetchone()
    db.commit()
    cursor.close()
    if not updated_item:
        raise HTTPException(status_code=404, detail="Order item not found")
    return updated_item


# ---------- DELETE ----------
@router.delete("/{order_id}/{items_id}")
def delete_order_item(order_id: int, items_id: int, db: connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(
        "DELETE FROM order_items WHERE order_id = %s AND items_id = %s RETURNING order_id;",
        (order_id, items_id)
    )
    deleted = cursor.fetchone()
    db.commit()
    cursor.close()
    if not deleted:
        raise HTTPException(status_code=404, detail="Order item not found")
    return {"message": "Order item deleted successfully"}
