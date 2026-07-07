"""
routers/products.py
--------------------
CRUD endpoints for the "products" table.
Same pattern as customers.py - only column names change.
"""

from fastapi import APIRouter, Depends, HTTPException
from psycopg2.extensions import connection
from database import get_db
from schemas import ProductCreate, Product

router = APIRouter(prefix="/products", tags=["Products"])


# ---------- CREATE ----------
@router.post("/", response_model=Product)
def create_product(product: ProductCreate, db: connection = Depends(get_db)):
    cursor = db.cursor()
    query = """
        INSERT INTO products (p_name, category, price, stock, brand)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING *;
    """
    cursor.execute(query, (product.p_name, product.category, product.price, product.stock, product.brand))
    new_product = cursor.fetchone()
    db.commit()
    cursor.close()
    return new_product


# ---------- READ ALL ----------
@router.get("/", response_model=list[Product])
def get_products(db: connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products ORDER BY p_id;")
    products = cursor.fetchall()
    cursor.close()
    return products


# ---------- READ ONE ----------
@router.get("/{p_id}", response_model=Product)
def get_product(p_id: int, db: connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products WHERE p_id = %s;", (p_id,))
    product = cursor.fetchone()
    cursor.close()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# ---------- UPDATE ----------
@router.put("/{p_id}", response_model=Product)
def update_product(p_id: int, product: ProductCreate, db: connection = Depends(get_db)):
    cursor = db.cursor()
    query = """
        UPDATE products
        SET p_name = %s, category = %s, price = %s, stock = %s, brand = %s
        WHERE p_id = %s
        RETURNING *;
    """
    cursor.execute(query, (product.p_name, product.category, product.price, product.stock, product.brand, p_id))
    updated_product = cursor.fetchone()
    db.commit()
    cursor.close()
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product


# ---------- DELETE ----------
@router.delete("/{p_id}")
def delete_product(p_id: int, db: connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM products WHERE p_id = %s RETURNING p_id;", (p_id,))
    deleted = cursor.fetchone()
    db.commit()
    cursor.close()
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": f"Product {p_id} deleted successfully"}
