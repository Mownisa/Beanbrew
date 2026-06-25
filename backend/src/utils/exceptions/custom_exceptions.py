class CoffeeShopBaseException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class CustomerNotFoundException(CoffeeShopBaseException):
    def __init__(self, customer_id: int):
        super().__init__(f"Customer with ID {customer_id} not found", status_code=404)


class AgentException(CoffeeShopBaseException):
    def __init__(self, message: str):
        super().__init__(message, status_code=500)


class PIIDetectionError(Exception):
    def __init__(self, message: str = "Sensitive information detected in input."):
        self.message = message
        super().__init__(message)
