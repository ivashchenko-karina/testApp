from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI(title="Orders Service", version="0.1.0")

CATALOG_SERVICE_URL = "http://127.0.0.1:5001/products"
ORDERS = {}

class OrderCreate(BaseModel):
    order_id: str
    product_id: str
    quantity: int = 1

@app.post("/orders", status_code=201)
def create_order(order: OrderCreate):
    try:
        response = requests.get(f"{CATALOG_SERVICE_URL}/{order.product_id}", timeout=2)
        if response.status_code == 404:
            raise HTTPException(status_code=400, detail="Товар не існує")
        
        product_data = response.json()
        if product_data["stock"] < order.quantity:
            raise HTTPException(status_code=400, detail="Недостатньо товару на складі")

        total_price = product_data["price"] * order.quantity
        new_order = {
            "order_id": order.order_id,
            "product_name": product_data["name"],
            "quantity": order.quantity,
            "total_price": total_price,
            "status": "Created"
        }
        ORDERS[order.order_id] = new_order
        return new_order

    except requests.exceptions.RequestException:
        raise HTTPException(status_code=503, detail="Сервіс каталогу недоступний")

@app.get("/orders/{order_id}")
def get_order(order_id: str):
    """Отримати інформацію про замовлення за його ID """
    order = ORDERS.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Замовлення не знайдено")
    return order