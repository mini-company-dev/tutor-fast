class CustomException(Exception):
    def __init__(self, message: str):
        self.code = 0
        self.message = message
        super().__init__(message)
