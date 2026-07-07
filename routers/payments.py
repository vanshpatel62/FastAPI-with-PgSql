"""
routers/payments.py
--------------------
CRUD endpoints for the "payments" table.
Same pattern again - only column names/table change.
"""

from fastapi import APIRouter, Depends, HTTPException
from psycopg2.extensions import connection
from database import get_db
from schemas import PaymentCreate, Payment

router = APIRouter(prefix="/payments", tags=["Payments"])


# ---------- CREATE ----------
@router.post("/", response_model=Payment)
def create_payment(payment: PaymentCreate, db: connection = Depends(get_db)):
    cursor = db.cursor()
    query = """
        INSERT INTO payments (transaction_id, order_id, amount, payment_method, payment_status)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING *;
    """
    cursor.execute(query, (
        payment.transaction_id, payment.order_id, payment.amount,
        payment.payment_method, payment.payment_status
    ))
    new_payment = cursor.fetchone()
    db.commit()
    cursor.close()
    return new_payment


# ---------- READ ALL ----------
@router.get("/", response_model=list[Payment])
def get_payments(db: connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM payments ORDER BY payment_id;")
    payments = cursor.fetchall()
    cursor.close()
    return payments


# ---------- READ ONE ----------
@router.get("/{payment_id}", response_model=Payment)
def get_payment(payment_id: int, db: connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM payments WHERE payment_id = %s;", (payment_id,))
    payment = cursor.fetchone()
    cursor.close()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


# ---------- UPDATE ----------
@router.put("/{payment_id}", response_model=Payment)
def update_payment(payment_id: int, payment: PaymentCreate, db: connection = Depends(get_db)):
    cursor = db.cursor()
    query = """
        UPDATE payments
        SET transaction_id = %s, order_id = %s, amount = %s,
            payment_method = %s, payment_status = %s
        WHERE payment_id = %s
        RETURNING *;
    """
    cursor.execute(query, (
        payment.transaction_id, payment.order_id, payment.amount,
        payment.payment_method, payment.payment_status, payment_id
    ))
    updated_payment = cursor.fetchone()
    db.commit()
    cursor.close()
    if not updated_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return updated_payment


# ---------- DELETE ----------
@router.delete("/{payment_id}")
def delete_payment(payment_id: int, db: connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM payments WHERE payment_id = %s RETURNING payment_id;", (payment_id,))
    deleted = cursor.fetchone()
    db.commit()
    cursor.close()
    if not deleted:
        raise HTTPException(status_code=404, detail="Payment not found")
    return {"message": f"Payment {payment_id} deleted successfully"}
