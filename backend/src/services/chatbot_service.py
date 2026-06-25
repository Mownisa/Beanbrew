from sqlalchemy.orm import Session

from src.agent import agent as agent_module
from src.repositories.customer_repository import get_customer_by_id
from src.utils.exceptions.custom_exceptions import (
    CustomerNotFoundException,
    PIIDetectionError,
    CoffeeShopBaseException,
)
from src.utils.pii_guard import apply_pii_guardrails
from src.utils.response import Response
from src.utils.error_logger import log_error
from src.models.models import ChatResponse
import traceback


async def handle_message(
    customer_id: int,
    user_message: str,
    db: Session,
) -> ChatResponse:
    print(f"[SERVICE] Incoming request | customer_id={customer_id} | message={user_message}")

    try:
        # Step 1: Verify customer
        customer = get_customer_by_id(db, customer_id)
        if customer is None:
            raise CustomerNotFoundException(customer_id)
        print(f"[SERVICE] Customer found: {customer.name}")

        # Step 2: PII guardrails
        safe_message = apply_pii_guardrails(user_message)
        print(f"[SERVICE] Safe message: {safe_message}")

        # Step 3: Agent
        print("[SERVICE] Invoking agent...")
        llm_response = await agent_module.run(
            customer_id=customer_id,
            customer_name=customer.name,
            user_message=safe_message,
            db=db,
        )
        print(f"[SERVICE] Agent response: {llm_response}")

        # Step 4: Build response
        response_dict = Response.success_response(
            message="Request processed successfully",
            data={"response": llm_response},
            code=200,
        )
        return ChatResponse(**response_dict)

    except PIIDetectionError as e:
        print(f"[SERVICE] PII blocked: {e.message}")
        response_dict = Response.error_response(
            message="Sensitive information detected. Please rephrase your message.",
            code=400,
            error={"type": "PIIDetectionError"},
        )
        return ChatResponse(**response_dict)

    except CoffeeShopBaseException as e:
        log_error(db, "handle_message", "chatbot_service.py", e.message, traceback.format_exc())
        response_dict = Response.error_response(
            message=e.message,
            code=e.status_code,
            error={"type": type(e).__name__},
        )
        return ChatResponse(**response_dict)

    except Exception as e:
        log_error(db, "handle_message", "chatbot_service.py", str(e), traceback.format_exc())
        response_dict = Response.error_response(
            message="An unexpected error occurred.",
            code=500,
            error={"type": type(e).__name__},
        )
        return ChatResponse(**response_dict)
