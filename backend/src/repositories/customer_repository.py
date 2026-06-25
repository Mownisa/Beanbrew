from sqlalchemy.orm import Session
from src.repositories.schema import Customer, Order, OrderItem, MenuItem


def get_customer_by_id(db: Session, customer_id: int):
    return db.query(Customer).filter(
        Customer.customer_id == customer_id,
        Customer.is_active == True,  # noqa: E712
    ).first()


def get_customer_by_email(db: Session, email: str):
    return db.query(Customer).filter(Customer.email == email).first()


def create_customer(db: Session, name: str, email: str, hashed_password: str) -> Customer:
    customer = Customer(name=name, email=email, hashed_password=hashed_password)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def get_latest_order(db: Session, customer_id: int):
    return (
        db.query(Order)
        .filter(Order.customer_id == customer_id)
        .order_by(Order.created_at.desc())
        .first()
    )
