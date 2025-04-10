class DatabaseConnectionException(Exception):
    """Raised when there is an issue with the database connection."""
    def __init__(self, message="Unable to connect to the database."):
        super().__init__(message)
