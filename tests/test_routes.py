# tests/test_routes.py
import pytest

@pytest.mark.integration
def test_homepage(client):
    r = client.get("/")
    assert r.status_code == 200
    assert b"Cart" in r.data

@pytest.mark.integration
def test_add_to_cart_with_invalid_quantity_graceful(client):
    # Known bug: direct int() cast can raise on bad input
    # We expect 302 redirect with a flash error in a robust app.
    resp = client.post("/add-to-cart", data={"title": "1984", "quantity": "bad"})
    assert resp.status_code in (200, 302)

@pytest.mark.integration
@pytest.mark.xfail_bug(reason="Known bug: discount code is case sensitive")
def test_checkout_discount_code_case_insensitive(client):
    # Start by visiting checkout to set up a cart and session
    client.post("/add-to-cart", data={"title": "1984", "quantity": "1"})
    payload = {
        "name": "Test User",
        "email": "tu@example.com",
        "address": "1 Test St",
        "city": "Testville",
        "zip_code": "T35 7ZZ",
        "payment_method": "credit_card",
        "card_number": "4111111111111111",
        "expiry_date": "12/30",
        "cvv": "123",
        "discount_code": "save10",
    }
    resp = client.post("/process-checkout", data=payload, follow_redirects=True)
    # If implemented case-insensitively, the response would include a success flash
    assert b"Welcome discount applied" in resp.data
