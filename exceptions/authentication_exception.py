class AuthenticationException(Exception):
    """Raised when user authentication fails (invalid credentials)."""
    def __init__(self, message="Invalid username or password."):
        super().__init__(message)
