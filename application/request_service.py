from domain.service_request import ServiceRequest
from domain.exceptions import (
    DuplicateRequestError,
    InvalidInputError,
    RequestNotFoundError,
    UnauthorizedActionError,
)
from infrastructure.file_repository import FileRepository


class RequestService:
    ADMIN_PASSCODE = "admin123"

    def __init__(self, repository: FileRepository):
        self.repository = repository
        self.requests: list[ServiceRequest] = self.repository.load_all()

    def create_request(
        self, request_id: str, employee_name: str, issue: str, priority: str
    ) -> ServiceRequest:
        clean_id = request_id.strip().upper()
        if not clean_id:
            raise InvalidInputError("Request ID cannot be empty.")

        if any(req.request_id == clean_id for req in self.requests):
            raise DuplicateRequestError(f"Service Request with ID '{clean_id}' already exists.")

        new_request = ServiceRequest(clean_id, employee_name, issue, priority)
        self.requests.append(new_request)
        self.repository.save_all(self.requests)
        return new_request

    def view_requests(self) -> list[ServiceRequest]:
        return self.requests

    def search_request(self, request_id: str) -> ServiceRequest:
        clean_id = request_id.strip().upper()
        if not clean_id:
            raise InvalidInputError("Request ID cannot be empty.")

        for req in self.requests:
            if req.request_id == clean_id:
                return req
        raise RequestNotFoundError(f"Request '{clean_id}' not found.")

    def resolve_request(self, request_id: str, admin_code: str) -> ServiceRequest:
        if admin_code.strip() != self.ADMIN_PASSCODE:
            raise UnauthorizedActionError("Access denied: Only an admin can resolve service requests.")

        request = self.search_request(request_id)
        request.resolve()
        self.repository.save_all(self.requests)
        return request