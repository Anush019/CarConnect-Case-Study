class AdminNotFoundException(Exception):
    """Raised when an admin user is not found."""
    def __init__(self, message="Admin not found."):
        super().__init__(message)
