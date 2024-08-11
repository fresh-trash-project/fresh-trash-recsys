from pydantic import BaseModel


class ProductProfileRequest(BaseModel):
    product_id: int
    category: int
    title: str
    content: str
