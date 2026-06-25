from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.repositories.database import get_db
from src.models.models import ChatRequest, ChatResponse
from src.services.chatbot_service import handle_message
from src.utils.auth import get_current_customer
from src.repositories.schema import Customer
from src.utils.error_logger import log_error
from src.utils.response import Response
import traceback

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    try:
        return await handle_message(
            customer_id=current_customer.customer_id,
            user_message=payload.message,
            db=db,
        )
    except Exception as e:
        log_error(db, "chat", "chatbot_route.py", str(e), traceback.format_exc())
        response_dict = Response.error_response("Internal server error", 500)
        return ChatResponse(**response_dict)
