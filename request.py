from pydantic import BaseModel


class ProductProfileRequest(BaseModel):
    file_name: str
    category: int
    title: str
    content: str
