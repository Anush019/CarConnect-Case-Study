class ReservationException(Exception):
    """Raised when there is an issue with reservations."""
    def __init__(self, message="Error in processing the reservation."):
        super().__init__(message)
