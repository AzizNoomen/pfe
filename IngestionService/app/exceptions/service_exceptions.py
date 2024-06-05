class OopsNoDBError(Exception):
    """Raised when DB is not running"""

    def __init__(self, message="No DB is found"):
        self.message = message
        super().__init__(self.message)

