from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.settings import config
from src.repositories.database import test_connection
from src.migrations.create_tables import Migration
from src.migrations.seeder import Seeder
from src.routes.auth_route import router as auth_router
from src.routes.chatbot_route import router as chat_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="BeanBrew ☕ Chatbot API",
        version="1.0.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth_router)
    app.include_router(chat_router)

    @app.get("/health")
    def health():
        return {"status": "ok", "service": "beanbrew-chatbot-api"}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    print("[BeanBrew] Starting up...")
    test_connection()
    Migration().create_tables()
    Seeder().seed_data()
    print("[BeanBrew] Ready! 🚀")

    uvicorn.run("main:app", host=config.HOST, port=config.PORT, reload=config.DEBUG)
