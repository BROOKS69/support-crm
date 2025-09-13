"""
API tests for Support CRM Backend.

This module contains comprehensive tests for all API endpoints using pytest
and FastAPI's TestClient. Tests cover authentication, CRUD operations,
and reporting functionality.

Run tests with:
    pytest test_api.py

Note: Tests are interdependent and should be run in order. They create
test data that subsequent tests depend on.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

# Create test client
client = TestClient(app)

def test_root():
    """
    Test the root endpoint returns welcome message.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Support CRM Backend API"}

def test_register():
    """
    Test user registration endpoint.

    Creates a test user account for use in subsequent tests.
    """
    response = client.post("/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass",
        "role": "agent"
    })
    assert response.status_code == 200
    assert "username" in response.json()

def test_login():
    """
    Test user login and JWT token generation.

    Returns the access token for use in authenticated requests.
    """
    response = client.post("/auth/login", data={
        "username": "testuser",
        "password": "testpass"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    return response.json()["access_token"]

def test_create_customer():
    """
    Test customer creation endpoint.

    Creates a test customer and returns the customer ID for use in ticket tests.
    """
    token = test_login()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/customers/", json={
        "name": "Test Customer",
        "email": "customer@example.com",
        "phone": "1234567890",
        "company": "Test Co",
        "notes": "Test notes"
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Customer"
    return response.json()["id"]

def test_get_customers():
    """
    Test customers list retrieval endpoint.
    """
    token = test_login()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/customers/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_ticket():
    """
    Test ticket creation endpoint.

    Creates a test ticket and returns the ticket ID for use in log tests.
    """
    token = test_login()
    headers = {"Authorization": f"Bearer {token}"}
    customer_id = test_create_customer()
    response = client.post("/tickets/", json={
        "title": "Test Ticket",
        "description": "Test description",
        "priority": "high",
        "status": "open",
        "customer_id": customer_id,
        "assigned_agent_id": None
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Ticket"
    return response.json()["id"]

def test_get_tickets():
    """
    Test tickets list retrieval endpoint.
    """
    token = test_login()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/tickets/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_log():
    """
    Test communication log creation endpoint.
    """
    token = test_login()
    headers = {"Authorization": f"Bearer {token}"}
    ticket_id = test_create_ticket()
    response = client.post("/logs/", json={
        "type": "call",
        "content": "Test log content",
        "ticket_id": ticket_id
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["type"] == "call"

def test_get_logs():
    """
    Test communication logs list retrieval endpoint.
    """
    token = test_login()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/logs/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_reports():
    """
    Test ticket summary report endpoint.
    """
    token = test_login()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/reports/tickets-summary", headers=headers)
    assert response.status_code == 200
    assert "total_tickets" in response.json()
