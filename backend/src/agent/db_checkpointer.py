from __future__ import annotations
import logging
from contextlib import asynccontextmanager
from src.settings import config

logger = logging.getLogger(__name__)


@asynccontextmanager
async def get_checkpointer():
    from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
    async with AsyncPostgresSaver.from_conn_string(config.POSTGRES_CONN_STRING) as checkpointer:
        await checkpointer.setup()
        logger.info("[db_checkpointer] AsyncPostgresSaver ready.")
        yield checkpointer


def make_thread_id(customer_id: int) -> str:
    return f"beanbrew-customer-{customer_id}"
