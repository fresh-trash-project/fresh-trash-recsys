# 🌱 중고 상품 플랫폼 Fresh Trash의 추천 시스템

## API Documentation

- [FreshTrash-RecSys API Documentation](https://documenter.getpostman.com/view/11961003/2sA3s3JXc3)

## Tech Stacks

### Backend
<p>
    <img src="https://github.com/user-attachments/assets/16533b6f-0cbf-4698-aec5-a8563485f394" width=15% align="middle">
    <img src="https://github.com/user-attachments/assets/b2ffe80d-7603-4f7c-ad3c-b412bf926b49" width=15% align="middle">
    <img src="https://github.com/user-attachments/assets/d61f0fd6-9ce0-4c99-826a-df76ace71d6c" width=15% align="middle">
    <img src="https://github.com/user-attachments/assets/75121f95-3ae5-40e0-af3f-57f6196939d9" width=20% align="middle">
</p>

- **FastAPI**, **Uvicorn** 로 서버를 구축했습니다.
- **SQLAlchemy** 로 객체 지향 데이터 로직을 작성했습니다.
- Huggigface의 **Transformers** 를 통해 pre-trained tokenizer를 추천 시스템 구현에 활용했습니다.

### Database

<p>
   <img width=15% src="https://github.com/fresh-trash-project/fresh-trash-backend/assets/82129206/a25f6bf9-3ee0-490b-a056-177f2d2674ef" alt="mariadb" />
</p>

- **MariaDB** 를 데이터베이스로 사용합니다.

### DevOps

<p>
   <img width=13% src="https://github.com/user-attachments/assets/d6a69903-1069-4d7f-bb18-20ade101927f" alt="docker" />
</p>

- **Docker** 로 일관성있는 개발 환경을 구축합니다.
