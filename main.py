import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import crud, models
from database import SessionLocal, engine
from request import ProductProfileRequest

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

"""
상품/경매 프로필 추가 및 수정
"""
@app.put("/profile/")
def create_or_update_profile(request: ProductProfileRequest):
    crud.create_or_update_profile(file_name=request.file_name, category=request.category, title=request.title, content=request.content)

"""
상품 구매
1. 구매 횟수 + 1
2. 회원 프로필 누적 합 계산
"""
@app.put("/product-purchase/{product_id}/{member_id}/")
def handle_product_purchase(product_id: int, member_id: int, db: Session = Depends(get_db)):
    crud.update_member_for_product_puchase(db, member_id, product_id)

"""
경매 낙찰 구매
1. 구매 횟수 + 1
2. 회원 프로필 누적 합 계산
"""
@app.put("/auction-purchase/{auction_id}/{member_id}/")
def handle_auction_purchase(auction_id: int, member_id: int, db: Session = Depends(get_db)):
    crud.update_member_for_auction_puchase(db, member_id, auction_id)

"""
상품 추천
"""
@app.get("/rec-sys/products/{member_id}/")
def recommended_products(member_id: int, limit: int, db: Session = Depends(get_db)):
    return crud.get_recommended_products(db, member_id, limit)

"""
경매 추천
"""
@app.get("/rec-sys/auctions/{member_id}/")
def recommended_auctions(member_id: int, limit: int, db: Session = Depends(get_db)):
    return crud.get_recommended_auctions(db, member_id, limit)

"""
테스트 데이터의 프로필 데이터 추가를 위해 사용
"""
@app.put("/initial-profile/")
def initialize_product_profile(db: Session = Depends(get_db)):
    crud.initialize_product_and_auction_profile(db)
    crud.initialize_member_profile(db)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=9080)
