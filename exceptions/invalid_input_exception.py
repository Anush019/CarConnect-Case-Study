class InvalidInputException(Exception):
    """Raised when input data is invalid (missing or incorrect format)."""
    def __init__(self, message="Invalid input provided."):
        super().__init__(message)
