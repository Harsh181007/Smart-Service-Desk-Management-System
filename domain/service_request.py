from domain.exceptions import (
    InvalidInputError,
    InvalidPriorityError,
    InvalidStatusError,
    RequestAlreadyResolvedError,
)


class ServiceRequest:
    VALID_PRIORITIES = {"LOW", "MEDIUM", "HIGH"}
    STATUS_OPEN = "OPEN"
    STATUS_RESOLVED = "RESOLVED"
    VALID_STATUSES = {STATUS_OPEN, STATUS_RESOLVED}

    def __init__(
        self,
        request_id: str,
        employee_name: str,
        issue: str,
        priority: str,
        status: str = STATUS_OPEN,
    ):
        clean_id = request_id.strip().upper() if isinstance(request_id, str) else ""
        clean_name = employee_name.strip() if isinstance(employee_name, str) else ""
        clean_issue = issue.strip() if isinstance(issue, str) else ""
        normalized_priority = priority.strip().upper() if isinstance(priority, str) else ""
        normalized_status = status.strip().upper() if isinstance(status, str) else ""

        if not clean_id or not clean_name or not clean_issue:
            raise InvalidInputError("Request ID, Employee Name, and Issue cannot be empty.")

        if clean_name.isdigit():
            raise InvalidInputError("Employee Name cannot contain only numbers.")

        if normalized_priority not in self.VALID_PRIORITIES:
            raise InvalidPriorityError("Priority must be LOW, MEDIUM or HIGH.")

        if normalized_status not in self.VALID_STATUSES:
            raise InvalidStatusError("Status must be OPEN or RESOLVED.")

        self.request_id = clean_id
        self.employee_name = clean_name
        self.issue = clean_issue
        self.priority = normalized_priority
        self.status = normalized_status

    def resolve(self) -> None:
        """Encapsulates the state transition from OPEN to RESOLVED."""
        if self.status == self.STATUS_RESOLVED:
            raise RequestAlreadyResolvedError(f"Request {self.request_id} is already RESOLVED.")
        self.status = self.STATUS_RESOLVED

    def to_dict(self) -> dict:
        return {
            "request_id": self.request_id,
            "employee_name": self.employee_name,
            "issue": self.issue,
            "priority": self.priority,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ServiceRequest":
        if not isinstance(data, dict):
            raise InvalidInputError("Corrupted record format in storage.")
        return cls(
            request_id=data["request_id"],
            employee_name=data["employee_name"],
            issue=data["issue"],
            priority=data["priority"],
            status=data.get("status", cls.STATUS_OPEN),
        )