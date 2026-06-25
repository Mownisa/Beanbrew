from src.repositories.database import Base, engine
import src.repositories.schema  # noqa: F401 — registers all ORM models with Base


class Migration:
    def create_tables(self):
        Base.metadata.create_all(bind=engine)
        print("[Migration] Tables checked/created.")
