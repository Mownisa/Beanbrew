import traceback
from datetime import datetime
from sqlalchemy.orm import Session
from src.repositories.schema import ErrorLog


def log_error(
    db: Session,
    function_name: str,
    file_name: str,
    error_message: str,
    stack_trace: str = "",
):
    try:
        log = ErrorLog(
            function_name=function_name,
            file_name=file_name,
            error_message=error_message,
            stack_trace=stack_trace,
            timestamp=datetime.utcnow(),
        )
        db.add(log)
        db.commit()
    except Exception as e:
        print(f"[ErrorLogger] Failed to log error: {e}")
