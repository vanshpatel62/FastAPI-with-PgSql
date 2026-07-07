"""
routers/customers.py
---------------------
All the CRUD (Create, Read, Update, Delete) endpoints for the "customers" table.
"""

from fastapi import APIRouter, Depends, HTTPException   # APIRouter = a mini FastAPI app we plug into main.py
from psycopg2.extensions import connection               # just used for type-hinting the db connection (not required, only helps readability)
from database import get_db
from schemas import CustomerCreate, Customer

router = APIRouter(
    prefix="/customers",     # every path below gets "/customers" added in front automatically
    tags=["Customers"]       # groups these endpoints together under "Customers" in the /docs page
)


# ---------- CREATE (INSERT) ----------
@router.post("/", response_model=Customer)   # response_model = the shape of data we promise to return
def create_customer(customer: CustomerCreate, db: connection = Depends(get_db)):
    cursor = db.cursor()                     # a cursor is what lets us run SQL commands on the connection
    query = """
        INSERT INTO customers (name, email, city)
        VALUES (%s, %s, %s)
        RETURNING *;
    """
    # %s are placeholders - psycopg2 safely inserts the real values here (protects against SQL injection)
    cursor.execute(query, (customer.name, customer.email, customer.city))
    new_customer = cursor.fetchone()         # get the row that was just inserted (because of RETURNING *)
    db.commit()                              # commit = actually save the change to the database
    cursor.close()
    return new_customer


# ---------- READ ALL ----------
@router.get("/", response_model=list[Customer])
def get_customers(db: connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM customers ORDER BY cust_id;")
    customers = cursor.fetchall()            # fetchall = get every matching row as a list
    cursor.close()
    return customers


# ---------- READ ONE ----------
@router.get("/{cust_id}", response_model=Customer)
def get_customer(cust_id: int, db: connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM customers WHERE cust_id = %s;", (cust_id,))
    customer = cursor.fetchone()
    cursor.close()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


# ---------- UPDATE ----------
@router.put("/{cust_id}", response_model=Customer)
def update_customer(cust_id: int, customer: CustomerCreate, db: connection = Depends(get_db)):
    cursor = db.cursor()
    query = """
        UPDATE customers
        SET name = %s, email = %s, city = %s
        WHERE cust_id = %s
        RETURNING *;
    """
    cursor.execute(query, (customer.name, customer.email, customer.city, cust_id))
    updated_customer = cursor.fetchone()
    db.commit()
    cursor.close()
    if not updated_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return updated_customer


# ---------- DELETE ----------
@router.delete("/{cust_id}")
def delete_customer(cust_id: int, db: connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM customers WHERE cust_id = %s RETURNING cust_id;", (cust_id,))
    deleted = cursor.fetchone()
    db.commit()
    cursor.close()
    if not deleted:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": f"Customer {cust_id} deleted successfully"}
