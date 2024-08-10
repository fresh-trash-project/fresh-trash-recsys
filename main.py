from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

"""
GET http://localhost:9080/api/

Content-Type: application/json
{
	"name":"joo",
	"price": 1000
}
"""
@app.get("/api/")
def create_item(item: Item):
    # 데이터베이스에 새로운 아이템 생성 로직
    return {"message": "Item created", "item": item}
