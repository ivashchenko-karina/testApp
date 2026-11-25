import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(
    title="MiniShop Catalog Service",
    version="1.0.0"
)


class Product(BaseModel):
    id: int
    name: str
    price: float
    description: str = ""


products = {
    1: Product(
        id=1,
        name="Laptop",
        price=25000.0,
        description="Business laptop"
    ),
    2: Product(
        id=2,
        name="Smartphone",
        price=15000.0,
        description="Android smartphone"
    ),
    3: Product(
        id=3,
        name="Headphones",
        price=2000.0,
        description="Wireless headphones"
    )
}


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "catalog"
    }


@app.get("/products")
def get_products():
    return list(products.values())


@app.get("/products/{product_id}")
def get_product(product_id: int):
    product = products.get(product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product

@app.get("/instance")
def instance():
    return {
        "service": "catalog",
        "hostname": os.getenv("HOSTNAME", "local")
    }