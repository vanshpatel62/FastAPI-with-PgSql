# FastAPI + PostgreSQL CRUD (Beginner Project)

Simple CRUD API for your existing 5-table e-commerce database
(customers, products, orders, order_items, payments).

## File structure

```
fastapi-pgsql-crud/
├── main.py              # starts the app, connects all routers
├── database.py           # opens/closes the PostgreSQL connection
├── schemas.py             # Pydantic models (input/output data validation)
├── requirements.txt        # Python packages needed
├── .env.example             # template for your DB credentials
└── routers/
    ├── customers.py       # /customers   endpoints
    ├── products.py         # /products    endpoints
    ├── orders.py            # /orders      endpoints
    ├── order_items.py        # /order-items endpoints
    └── payments.py            # /payments    endpoints
```

## How to run

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and fill in your real database name/user/password:
   ```
   cp .env.example .env
   ```

3. Start the server:
   ```
   uvicorn main:app --reload
   ```

4. Open your browser at:
   ```
   http://127.0.0.1:8000/docs
   ```
   This is Swagger UI - an auto-generated page where you can test every
   Create/Read/Update/Delete endpoint by clicking buttons, no Postman needed.

## Notes for a beginner

- Every route file (`routers/*.py`) follows the exact same 5-endpoint pattern:
  `POST /` (create), `GET /` (read all), `GET /{id}` (read one),
  `PUT /{id}` (update), `DELETE /{id}` (delete).
  Once you understand `customers.py`, the other four are basically the same idea.
- `order_items.py` is slightly different because that table's primary key is
  TWO columns together (`order_id` + `items_id`), so its URLs need both, e.g.
  `/order-items/3/7`.
- Parts marked **OPTIONAL** in the code comments (CORS, foreign-key try/except,
  `.env` usage) are not required to make the CRUD work - they're good habits
  you can add or remove depending on what your project needs.
- This uses raw SQL through `psycopg2` (matches the SQL you already wrote),
  not an ORM like SQLAlchemy. That's intentional - it's easier to see
  exactly what SQL is running while you're still learning.
