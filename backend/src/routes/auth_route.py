from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.repositories.database import get_db
from src.repositories.customer_repository import get_customer_by_email, create_customer
from src.models.models import RegisterRequest, LoginRequest, TokenResponse, CustomerOut
from src.utils.auth import hash_password, verify_password, create_access_token, get_current_customer
from src.repositories.schema import Customer

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    if get_customer_by_email(db, payload.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    customer = create_customer(
        db,
        name=payload.name,
        email=payload.email,
        hashed_password=hash_password(payload.password),
    )
    token = create_access_token({"sub": str(customer.customer_id)})
    return TokenResponse(
        access_token=token,
        customer_id=customer.customer_id,
        name=customer.name,
        email=customer.email,
    )


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    customer = get_customer_by_email(db, payload.email)
    if not customer or not verify_password(payload.password, customer.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    token = create_access_token({"sub": str(customer.customer_id)})
    return TokenResponse(
        access_token=token,
        customer_id=customer.customer_id,
        name=customer.name,
        email=customer.email,
    )


@router.get("/me", response_model=CustomerOut)
def me(current: Customer = Depends(get_current_customer)):
    return current
