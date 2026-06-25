import uuid
from datetime import datetime, timezone


class Response:
    @staticmethod
    def success_response(message: str, data=None, code: int = 200) -> dict:
        return {
            "code": code,
            "status": "success",
            "message": message,
            "data": data,
            "error": None,
            "request_id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    @staticmethod
    def error_response(message: str, code: int = 500, error=None) -> dict:
        return {
            "code": code,
            "status": "error",
            "message": message,
            "data": None,
            "error": error,
            "request_id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
