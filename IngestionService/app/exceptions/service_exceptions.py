class DatabaseConnectionError(Exception):
    """Raised when DB is not running"""

    def __init__(self, message: str ="Database connection error"):
        self.message = message
        super().__init__(self.message)

