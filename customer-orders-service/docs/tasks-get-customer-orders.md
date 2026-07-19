# Task List: Get Customer Orders

## T001: Define orders schema

**Files:** src/db/models.py, src/db/migrations/2026_07_20_create_orders_table.sql
**Action:** 
Define an Orders model with fields:
- id (primary key)
- customer_id
- order_date
- amount
- status

Create a migration file that creates the orders table with these columns in SQLite/PostgreSQL.

**Verification:** 
- Run the migration script against the local database.
- Confirm the orders table exists with the correct columns (using a DB browser or sqlite3/psql).

**Done:** 
- Orders model is defined.
- Orders table exists in the local database.

## T002: Implement OrdersRepository

**Files:** src/repositories/orders_repository.py
**Action:** 
Create OrdersRepository with methods:
- get_orders_by_customer(customer_id: str, status: Optional[str], page: int, page_size: int)
Use SQLAlchemy or direct queries to fetch paginated orders from the orders table.

**Verification:** 
- Write a small local script or temporary test that calls get_orders_by_customer with sample data.
- Confirm it returns the expected list of orders for a given customer.

**Done:** 
- OrdersRepository is implemented and can fetch paginated orders for a given customer from the local DB.

## T003: Implement GET /orders endpoint

**Files:** src/api/orders.py, src/main.py
**Action:** 
- Create a FastAPI router in src/api/orders.py with a GET /orders endpoint.
- The endpoint SHALL:
  - Read the authenticated customer id (for now, you can simulate or stub this).
  - Accept optional query parameters: status, page, page_size.
  - Call OrdersRepository.get_orders_by_customer and return JSON with:
    - list of orders
    - pagination metadata (page, page_size, total_count).

- Include the router in src/main.py (app.include_router(...)).

**Verification:** 
- Run uvicorn src.main:app --reload.
- Call http://localhost:8000/orders (using browser, curl, or Postman).
- Confirm the response shape matches the Feature Spec and Technical Plan.

**Done:** 
- GET /orders endpoint is functional and returns data from the repository with pagination and filters.

## T004: Add unit tests for OrdersRepository

**Files:** tests/test_orders_repository.py
**Action:** 
- Write unit tests that:
  - Insert sample orders into a test database.
  - Call OrdersRepository.get_orders_by_customer with different parameters.
  - Assert that:
    - Only orders for the given customer are returned.
    - Status filtering works.
    - Pagination returns correct subsets.

**Verification:** 
- Run pytest tests/test_orders_repository.py.
- All tests pass.

**Done:** 
- Unit tests cover core repository logic for filtering and pagination.

## T005: Add integration tests for GET /orders

**Files:** tests/test_orders_endpoint.py
**Action:** 
- Use FastAPI TestClient or similar to:
  - Seed the test database with sample orders.
  - Call GET /orders for a given customer.
  - Test edge cases:
    - Customer with no orders.
    - Unauthenticated request (expect 401).
    - Invalid page number (expect 400).

**Verification:** 
- Run pytest tests/test_orders_endpoint.py.
- All tests pass.

**Done:** 
- Integration tests validate GET /orders behavior against edge cases and success criteria. 