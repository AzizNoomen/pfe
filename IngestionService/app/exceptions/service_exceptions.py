class OopsNoDBError(Exception):
    """Raised when DB is not running"""

    def __init__(self, message="No DB is found"):
        self.message = message
        super().__init__(self.message)


class ModelServiceUnavailable(Exception):
    def __init__(self, message="Model service unavailable"):
        self.message = message
        super().__init__(self.message)


class NoConceptsExtracted(Exception):
    def __init__(self, message="No concept was extracted"):
        self.message = message
        super().__init__(self.message)


class NoTextExtracted(Exception):
    def __init__(self, message="No text was extracted from the documents"):
        self.message = message
        super().__init__(self.message)