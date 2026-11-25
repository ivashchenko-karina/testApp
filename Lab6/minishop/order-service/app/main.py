import os
from itertools import count

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI(
    title="MiniShop Order Service",
    version="1.0.0"
)

CATALOG_URL = os.getenv(
    "CATALOG_URL",
    "http://localhost:8001"
)

orders = {}
order_ids = count(1)


class OrderRequest(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "order"
    }


@app.post("/orders", status_code=201)
def create_order(request: OrderRequest):
    try:
        response = httpx.get(
            f"{CATALOG_URL}/products/{request.product_id}",
            timeout=3.0
        )
        response.raise_for_status()

    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        raise HTTPException(
            status_code=502,
            detail="Catalog service error"
        )

    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="Catalog service unavailable"
        )

    product = response.json()
    order_id = next(order_ids)

    order = {
        "id": order_id,
        "product_id": request.product_id,
        "product_name": product["name"],
        "quantity": request.quantity,
        "unit_price": product["price"],
        "total_price": product["price"] * request.quantity,
        "status": "created"
    }

    orders[order_id] = order
    return order


@app.get("/orders")
def get_orders():
    return list(orders.values())


@app.get("/orders/{order_id}")
def get_order(order_id: int):
    order = orders.get(order_id)

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order

@app.get("/instance")
def instance():
    return {
        "service": "order",
        "hostname": os.getenv("HOSTNAME", "local")
    }