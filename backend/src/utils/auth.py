from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.repositories.database import get_db
from src.repositories.schema import Customer
from src.settings import config

# ✅ Use Argon2 (fixes bcrypt 72-byte limit)
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours


# ─────────────────────────────────────────
# PASSWORD FUNCTIONS
# ─────────────────────────────────────────

def hash_password(password: str) -> str:
    if not isinstance(password, str):
        raise ValueError("Password must be a string")

    password = password.strip()

    if len(password) < 6:
        raise ValueError("Password must be at least 6 characters")

    if len(password) > 128:
        raise ValueError("Password too long (max 128 characters)")

    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    if not plain or not hashed:
        return False

    return pwd_context.verify(plain, hashed)


# ─────────────────────────────────────────
# JWT TOKEN
# ─────────────────────────────────────────

def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        config.SECRET_KEY,
        algorithm=ALGORITHM
    )


# ─────────────────────────────────────────
# AUTH DEPENDENCY
# ─────────────────────────────────────────

def get_current_customer(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Customer:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            config.SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        sub = payload.get("sub")
        if sub is None:
            raise credentials_exception

        customer_id = int(sub)

    except (JWTError, TypeError, ValueError):
        raise credentials_exception

    customer = (
        db.query(Customer)
        .filter(
            Customer.customer_id == customer_id,
            Customer.is_active == True,  # noqa: E712
        )
        .first()
    )

    if customer is None:
        raise credentials_exception

    return customer