import pytest
from online_bookstore_final_assessment.app import app, users


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_page(client):
    res = client.get("/")
    assert res.status_code == 200


def test_register_and_login_logout_flow(client):
    # Register
    res = client.post("/register", data={
        "email": "user@test.com",
        "password": "pw",
        "name": "User",
        "address": "123 Street"
    }, follow_redirects=True)
    assert b"Account created successfully" in res.data

    # Login
    res = client.post("/login", data={
        "email": "user@test.com",
        "password": "pw"
    }, follow_redirects=True)
    assert b"Logged in successfully" in res.data

    # Logout
    res = client.get("/logout", follow_redirects=True)
    assert b"Logged out successfully" in res.data


def test_duplicate_register(client):
    users.clear()
    client.post("/register", data={
        "email": "dup@test.com", "password": "pw", "name": "User"
    })
    res = client.post("/register", data={
        "email": "dup@test.com", "password": "pw", "name": "User"
    })
    assert b"already exists" in res.data


def test_add_and_remove_cart(client):
    # First register and login
    client.post("/register", data={"email": "c@test.com", "password": "pw", "name": "User"})
    client.post("/login", data={"email": "c@test.com", "password": "pw"})

    # Add book
    res = client.get("/add-to-cart/1", follow_redirects=True)
    assert b"Book added to cart" in res.data

    # Remove
    res = client.get("/remove-from-cart/1", follow_redirects=True)
    assert b"removed from your cart" in res.data


def test_checkout_success_and_failure(client):
    client.post("/register", data={"email": "o@test.com", "password": "pw", "name": "Order User"})
    client.post("/login", data={"email": "o@test.com", "password": "pw"})
    client.get("/add-to-cart/1")

    # Successful payment
    res = client.post("/checkout", data={
        "card_number": "12345678",
        "payment_method": "card",
        "address": "123 Street"
    }, follow_redirects=True)
    assert b"Order placed successfully" in res.data

    client.get("/add-to-cart/1")
    # Failing payment
    res = client.post("/checkout", data={
        "card_number": "1111",
        "payment_method": "card",
        "address": "123 Street"
    }, follow_redirects=True)
    assert b"Payment failed" in res.data


def test_account_and_update_profile(client):
    client.post("/register", data={"email": "p@test.com", "password": "pw", "name": "Profile User"})
    client.post("/login", data={"email": "p@test.com", "password": "pw"})

    res = client.get("/account")
    assert res.status_code == 200

    res = client.post("/update-profile", data={"name": "New Name"}, follow_redirects=True)
    assert b"Profile updated successfully" in res.data
