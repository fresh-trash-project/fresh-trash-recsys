from sqlalchemy import select
from sqlalchemy.orm import Session
from utils import Tokenizer, ndarray_to_text, text_to_ndarray, cos_sim
from models import Product, ProductProfile, MemberPurchaseProfile, ProductSellStatus


def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def get_product_with_profile(db: Session):
    return db.execute(select(Product, ProductProfile).filter(Product.id == ProductProfile.product_id).where(Product.sell_status == ProductSellStatus.ONGOING)).all()

def get_product_profile(db: Session, product_id: int):
    return db.query(ProductProfile).filter(ProductProfile.product_id == product_id).first()

def get_member_purchase_profile(db: Session, member_id: int):
    return db.query(MemberPurchaseProfile).filter(MemberPurchaseProfile.member_id == member_id).first()

def update_member_for_puchase(db: Session, member_id: int, product_id: int):
    # -- 구매 횟수 + 1
    member_profile = get_member_purchase_profile(db, member_id=member_id)
    member_profile.purchase_count += 1

    tokenizer = Tokenizer()

    # -- 회원 프로필 누적 합 조회 후 Numpy Array로 변환
    product_cumulative_sum = member_profile.product_cumulative_sum
    if product_cumulative_sum == None:
        product_cumulative_sum = tokenizer.get_empty_vector()
    else:
        product_cumulative_sum = text_to_ndarray(product_cumulative_sum)
    
    # -- 상품의 프로필 정보가 없다면 생성하여 추가
    product_profile = get_product_profile(db, product_id=product_id)
    product_vector = product_profile.profile
    if product_vector == None:
        buyed_product = get_product(db, product_id)
        product_vector = tokenizer.get_product_vector(f"{buyed_product.title} {buyed_product.content}", buyed_product.product_category.value)
        product_profile.profile = ndarray_to_text(product_vector)
    else:
        product_vector = text_to_ndarray(product_vector)
    
    # -- 구매한 상품의 프로필 정보를 누적한 후 저장
    product_cumulative_sum += product_vector
    member_profile.product_cumulative_sum = ndarray_to_text(product_cumulative_sum)
    db.commit()

def create_product_profile(db: Session, product_id:int, category: int, title: str, content: str):
    tokenizer = Tokenizer()
    product_vector = tokenizer.get_product_vector(f"{title} {content}", category)
    product_profile = ProductProfile(product_id=product_id, profile=ndarray_to_text(product_vector))
    db.add(product_profile)
    db.commit()

def update_product_profile(db: Session, product_id:int, category: int, title: str, content: str):
    db_product_profile = get_product_profile(db, product_id=product_id)
    tokenizer = Tokenizer()
    product_vector = tokenizer.get_product_vector(f"{title} {content}", category)
    db_product_profile.profile = ndarray_to_text(product_vector)
    db.commit()

def get_recommended_products(db: Session, member_id: int, limit: int):
    member_purchase_profile = get_member_purchase_profile(db, member_id)
    member_profile = text_to_ndarray(member_purchase_profile.product_cumulative_sum) / member_purchase_profile.purchase_count
    
    cosine_similarity_values = list(map(lambda x: (cos_sim(member_profile, text_to_ndarray(x[1].profile)).item(), x[0]), get_product_with_profile(db)))
    cosine_similarity_values.sort(key=lambda x: x[0], reverse=True)

    return {"products": [value[1] for value in cosine_similarity_values[:limit]]}

def initialize_product_profile(db: Session):
    product_profiles = list(map(lambda x: x[1], get_product_with_profile(db)))
    tokenizer = Tokenizer()
    for product_profile in product_profiles:
        product = get_product(db, product_profile.product_id)
        product_vector = tokenizer.get_product_vector(f"{product.title} {product.content}", product.product_category.value)
        product_profile.profile = ndarray_to_text(product_vector)
    db.commit()
