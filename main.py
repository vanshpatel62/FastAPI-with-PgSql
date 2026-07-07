"""
main.py
-------
This is the entry point of the whole API.
Run it with:  uvicorn main:app --reload
"""

from fastapi import FastAPI
from routers import customers, products, orders, order_items, payments

# Creates the FastAPI application object. "title" just shows up in the docs page - OPTIONAL, change/remove anytime.
app = FastAPI(title="E-Commerce CRUD API")

# ---------------------------------------------------------------------
# OPTIONAL: CORS (Cross-Origin Resource Sharing)
# Only needed IF a separate frontend app (React, Vue, plain HTML on a
# different port) will call this API from the browser. Not required for
# testing with /docs or Postman. Uncomment if/when you need it.
# ---------------------------------------------------------------------
# from fastapi.middleware.cors import CORSMiddleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],       # "*" means allow any website - fine for learning, NOT for real production
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# Plug in each table's set of CRUD routes.
# Because each router already has its own "prefix" (like /customers), we don't repeat it here.
app.include_router(customers.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(order_items.router)
app.include_router(payments.router)


# A simple "is it alive" route - OPTIONAL, just handy to check the server is running.
@app.get("/")
def root():
    return {"message": "API is running. Go to /docs to test all endpoints."}
