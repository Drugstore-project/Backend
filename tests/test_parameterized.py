import pytest
from app.schemas.user import UserCreate
from pydantic import ValidationError

# --- UNIT TESTS (No DB, pure logic/validation) ---

@pytest.mark.parametrize("email, is_valid", [
    ("test@example.com", True),
    ("user.name@domain.co", True),
    ("user+tag@domain.com", True),
    ("plainaddress", False),
    ("@missingusername.com", False),
    ("username@.com", False),
])
def test_user_email_validation(email, is_valid):
    """
    Unit test to verify Pydantic email validation.
    Does not require DB or API Client.
    """
    if is_valid:
        user = UserCreate(
            name="Test",
            email=email,
            password="password123",
            role_id=1
        )
        assert user.email == email
    else:
        with pytest.raises(ValidationError):
            UserCreate(
                name="Test",
                email=email,
                password="password123",
                role_id=1
            )

@pytest.mark.parametrize("password, is_valid", [
    ("123456", True),
    ("1234", False),
    ("", False),
    ("verylongpasswordthatisdefinitelysecure", True)
])
def test_user_password_validation(password, is_valid):
    """
    Unit test to verify Pydantic password length validation.
    """
    if is_valid:
        user = UserCreate(
            name="Test",
            email="test@example.com",
            password=password,
            role_id=1
        )
        assert user.password == password
    else:
        with pytest.raises(ValidationError):
            UserCreate(
                name="Test",
                email="test@example.com",
                password=password,
                role_id=1
            )

# --- INTEGRATION TESTS (Uses DB and Client) ---

@pytest.mark.parametrize("endpoint, method, expected_status", [
    ("/users/", "GET", 200),
    ("/products/", "GET", 200),
    ("/orders/", "GET", 200),
    ("/nonexistent/", "GET", 404),
])
def test_api_endpoints_availability(client, endpoint, method, expected_status):
    """
    Parameterized integration test to check availability of main endpoints.
    """
    if method == "GET":
        response = client.get(endpoint)
    elif method == "POST":
        response = client.post(endpoint)
    
    assert response.status_code == expected_status

