from infrastructure.file_repository import FileRepository
from application.request_service import RequestService
from domain.exceptions import ServiceDeskError


def display_menu() -> None:
    print("\nSMART SERVICE DESK SYSTEM")
    print("1. Create Service Request")
    print("2. View All Requests")
    print("3. Search Request")
    print("4. Resolve Request")
    print("5. Exit")


def main() -> None:
    repository = FileRepository("data/requests.json")
    service = RequestService(repository)

    try:
        while True:
            display_menu()
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                try:
                    req_id = input("Enter Request ID: ").strip()
                    emp_name = input("Enter Employee Name: ").strip()
                    issue = input("Enter Issue: ").strip()
                    priority = input("Enter Priority (LOW/MEDIUM/HIGH): ").strip()

                    service.create_request(req_id, emp_name, issue, priority)
                    print("Service Request created successfully.")
                except ServiceDeskError as err:
                    print(f"Error: {err}")

            elif choice == "2":
                requests = service.view_requests()
                if not requests:
                    print("No service requests found.")
                else:
                    for req in requests:
                        print(f"{req.request_id} | {req.employee_name} | {req.issue} | {req.priority} | {req.status}")

            elif choice == "3":
                req_id = input("Enter Request ID to search: ").strip()
                try:
                    req = service.search_request(req_id)
                    print(f"\nRequest ID   : {req.request_id}")
                    print(f"Employee Name: {req.employee_name}")
                    print(f"Issue        : {req.issue}")
                    print(f"Priority     : {req.priority}")
                    print(f"Status       : {req.status}")
                except ServiceDeskError as err:
                    print(f"Error: {err}")

            elif choice == "4":
                req_id = input("Enter Request ID to resolve: ").strip()
                admin_code = input("Enter Admin Passcode: ").strip()
                try:
                    service.resolve_request(req_id, admin_code)
                    print(f"Service Request {req_id.upper()} has been marked as RESOLVED.")
                except ServiceDeskError as err:
                    print(f"Error: {err}")

            elif choice == "5":
                print("Exiting Smart Service Desk System. Goodbye!")
                break

            else:
                print("Invalid choice. Please enter a number between 1 and 5.")
    except (KeyboardInterrupt, EOFError):
        print("\nSession interrupted. Exiting Smart Service Desk System safely.")


if __name__ == "__main__":
    main()