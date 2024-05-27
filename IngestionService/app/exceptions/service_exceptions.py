class OopsNoDBError(Exception):
    """Raised when DB is not running"""

    def __init__(self, message="No DB is found"):
        self.message = message
        super().__init__(self.message)


class ModelServiceConnectionError(Exception):
    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)


class ModelResultParsingError(Exception):
    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)
