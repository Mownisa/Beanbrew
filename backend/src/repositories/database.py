from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from src.settings import config


def get_database_url():
    url = config.DATABASE_URL
    url = url.replace("postgresql+psycopg://", "postgresql://")
    url = url.replace("postgresql+psycopg2://", "postgresql://")
    url = url.replace("postgres://", "postgresql://")
    url = url.replace("&channel_binding=require", "")
    return url


engine = create_engine(
    get_database_url(),
    pool_pre_ping=True,
    echo=config.DEBUG,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_connection() -> bool:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"[Database] Connection failed: {e}")
        raise SystemExit(1)