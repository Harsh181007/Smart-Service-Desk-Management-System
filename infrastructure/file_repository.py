import json
import os
from domain.exceptions import ServiceDeskError
from domain.service_request import ServiceRequest


class FileRepository:
    def __init__(self, file_path: str = "data/requests.json"):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        directory = os.path.dirname(self.file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump([], file)

    def load_all(self) -> list[ServiceRequest]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                content = file.read().strip()
                if not content:
                    return []
                raw_data = json.loads(content)
                if not isinstance(raw_data, list):
                    return []

                valid_requests: list[ServiceRequest] = []
                for item in raw_data:
                    try:
                        valid_requests.append(ServiceRequest.from_dict(item))
                    except (KeyError, TypeError, ValueError, ServiceDeskError):
                        continue
                return valid_requests
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            return []

    def save_all(self, requests: list[ServiceRequest]) -> None:
        self._ensure_file_exists()
        data = [req.to_dict() for req in requests]
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)