from utils import *
from config import LOGGER
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from models import Product, Member, ProductSellStatus


def get_product(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product == None:
        raise HTTPException(404, f'Product not found. Product ID is {product_id}') 
    return product

def get_ongoing_products(db: Session):
    return db.query(Product).where(Product.sell_status == ProductSellStatus.ONGOING).all()

def get_member(db: Session, member_id: int):
    member = db.query(Member).filter(Member.id == member_id).first()
    if member == None:
        raise HTTPException(404, f'Member not found. Mebmer ID is {member_id}') 
    return member

def get_members(db: Session):
    return db.query(Member).all()

def create_or_update_member_for_product_puchase(db: Session, member_id: int, product_id: int):
    # -- 구매 횟수 + 1
    member = get_member(db, member_id=member_id)
    member.product_purchase_count += 1

    # -- 회원 프로필 파일이 존재하면 해당 파일을 불러오고, 없다면 새로 생성
    tokenizer = Tokenizer()
    if FileUtils.existsFile(member.product_vector_file_name):
        product_cumulative_sum = load_numpy(member.product_vector_file_name)
    else:
        product_cumulative_sum = tokenizer.get_empty_vector()
    
    # -- 구매상품의 프로필 조회
    product = get_product(db, product_id=product_id)
    try:
        product_vector = load_numpy(product.profile_file_name)
    except:
        raise HTTPException(404, f'Product profile file not found. Product ID is {product_id}')
    
    # -- 구매한 상품의 프로필 정보를 누적한 후 저장
    product_cumulative_sum += product_vector
    save_numpy(member.product_vector_file_name, product_cumulative_sum)

def update_product_profile(file_name: str, category: int, title: str, content: str):
    # -- Vector 생성
    tokenizer = Tokenizer()
    product_vector = tokenizer.get_product_vector(f"{title} {content}", category)
    # -- 파일 저장
    save_numpy(file_name, product_vector)

def get_recommended_products(db: Session, member_id: int, limit: int):
    # -- 회원 프로필 조회
    member = get_member(db, member_id)
    import pdb
    pdb.set_trace()
    member_product_vector = load_numpy(member.product_vector_file_name)
    member_profile = member_product_vector / member.product_purchase_count
    
    # -- ONGOING 상태인 상품을 모두 조회하여 하나씩 코사인 유사도를 계산
    products = get_ongoing_products(db)
    cosine_similarity_values = []
    for idx, product in enumerate(products):
        try:
            cosine_similarity_values.append((cos_sim(member_profile, load_numpy(product.profile_file_name)), idx))
        except:
            LOGGER.warn(f'Product profile file not found. Product ID is {product.id}')
            cosine_similarity_values.append((-1, idx))
    
    cosine_similarity_values.sort(key=lambda x: x[0], reverse=True)

    return {"products": [products[value[1]] for value in cosine_similarity_values[:limit]]}

def initialize_product_profile(db: Session):
    products = get_ongoing_products(db)
    tokenizer = Tokenizer()
    for product in products:
        product_vector = tokenizer.get_product_vector(f"{product.title} {product.content}", product.product_category.value)
        save_numpy(product.profile_file_name, product_vector)

def initialize_member_profile(db: Session):
    members = get_members(db)
    tokenizer = Tokenizer()
    for member in members:
        save_numpy(member.product_vector_file_name, tokenizer.get_empty_vector())
        save_numpy(member.auction_vector_file_name, tokenizer.get_empty_vector())
