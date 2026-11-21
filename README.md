# Smart Service Desk Management System

A CLI-based IT support ticket management system built in Python using Domain-Driven Design (DDD), SOLID principles, Object-Oriented Programming, and JSON file persistence.

## Problem Statement
Organizations managing IT support tickets manually face lost requests, duplicate IDs, unauthorized status changes, and poor tracking. This application provides support staff with a reliable way to log, inspect, search, and resolve employee IT requests with persistent storage and role-based resolution checks.

## Implemented Features
- **Create Service Request:** Logs new tickets (`OPEN` by default) with duplicate ID prevention, input validation, and strict priority validation (`LOW`, `MEDIUM`, `HIGH`).
- **View All Requests:** Displays all stored requests cleanly.
- **Search Request:** Retrieves full details of a ticket using its unique Request ID.
- **Admin-Only Resolve Request:** Transitions `OPEN` tickets to `RESOLVED` only after verifying the support admin passcode (`admin123`) and persists changes immediately.
- **JSON Persistence & Corruption Recovery:** Automatically loads existing records on startup, handles missing/empty/malformed JSON files safely, and saves modifications to `data/requests.json`.

## Concepts Used
- **OOP:** Encapsulated `ServiceRequest` entity with state-transition methods (`resolve()`) and strict attribute invariants.
- **Exception Handling:** Custom domain exception hierarchy (`ServiceDeskError`, `RequestNotFoundError`, `DuplicateRequestError`, `InvalidPriorityError`, `InvalidStatusError`, `InvalidInputError`, `RequestAlreadyResolvedError`, `UnauthorizedActionError`) plus graceful `KeyboardInterrupt`/`EOFError` exit handling.
- **File Handling:** Safe JSON serialization/deserialization that recovers gracefully from missing, empty, or corrupted records.
- **SOLID & DDD:** Separation across Domain, Application, Infrastructure, and Presentation layers, with Dependency Inversion (`RequestService` depends on `FileRepository` passed via constructor).
- **Git Workflow:** Feature development isolated on `development` branch with incremental commits before merging into `main`.

## Project Folder Structure
```text
smart-service-desk/
├── domain/
│   ├── __init__.py
│   ├── service_request.py
│   └── exceptions.py
├── application/
│   ├── __init__.py
│   └── request_service.py
├── infrastructure/
│   ├── __init__.py
│   └── file_repository.py
├── data/
│   └── requests.json
├── main.py
├── README.md
└── .gitignore

Admin Passcode for Resolving Requests: admin123