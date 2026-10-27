from fastapi import FastAPI, HTTPException

app = FastAPI(title="Catalog Service", version="1.0.0")

# База даних товарів у пам'яті
PRODUCTS = {
    "P1": {"name": "Ноутбук", "price": 1200.0, "stock": 10},
    "P2": {"name": "Смартфон", "price": 800.0, "stock": 5},
    "P3": {"name": "Навушники", "price": 150.0, "stock": 0}
}

@app.get("/products/{product_id}")
def get_product(product_id: str):
    product = PRODUCTS.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Товар не знайдено")
    return product

