class ServiceDeskError(Exception):
    """Base exception for all service desk domain errors."""
    pass


class RequestNotFoundError(ServiceDeskError):
    """Raised when a service request ID does not exist."""
    pass


class DuplicateRequestError(ServiceDeskError):
    """Raised when attempting to create a request with an existing ID."""
    pass


class InvalidPriorityError(ServiceDeskError):
    """Raised when priority is not LOW, MEDIUM, or HIGH."""
    pass


class InvalidStatusError(ServiceDeskError):
    """Raised when status is not OPEN or RESOLVED."""
    pass


class InvalidInputError(ServiceDeskError):
    """Raised when required fields are empty or malformed."""
    pass


class RequestAlreadyResolvedError(ServiceDeskError):
    """Raised when attempting to resolve an already resolved request."""
    pass


class UnauthorizedActionError(ServiceDeskError):
    """Raised when a non-admin attempts a restricted operation."""
    pass