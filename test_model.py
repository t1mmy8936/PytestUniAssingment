import pytest
from online_bookstore_final_assessment.models import (
    Book, CartItem, Cart, User, Order, PaymentGateway, EmailService
)


def test_book_to_dict():
    book = Book(1, "Test Book", "Author", 9.99, "Fiction", 5)
    result = book.to_dict()
    assert result["title"] == "Test Book"
    assert result["price"] == 9.99


def test_cartitem_creation():
    book = Book(1, "Book", "Auth", 5.0, "Fiction", 2)
    item = CartItem(book, 3)
    assert item.quantity == 3
    assert item.book == book


def test_cart_add_remove_items():
    cart = Cart()
    book = Book(1, "Book", "Auth", 5.0, "Fiction", 2)
    cart.add_item(book, 2)
    assert cart.items[0].quantity == 2

    cart.add_item(book, 1)
    assert cart.items[0].quantity == 3

    cart.remove_item(book, 2)
    assert cart.items[0].quantity == 1

    cart.remove_item(book, 1)
    assert len(cart.items) == 0


def test_cart_total_and_clear():
    cart = Cart()
    b1 = Book(1, "B1", "A", 10, "Fiction", 1)
    b2 = Book(2, "B2", "B", 20, "Non-fiction", 1)
    cart.add_item(b1, 1)
    cart.add_item(b2, 2)
    assert cart.calculate_total() == 50

    cart.clear_cart()
    assert len(cart.items) == 0


def test_user_orders():
    user = User("test@test.com", "pw", "Test", "123 Street")
    order = Order(1, user.email, [], {}, {}, 0)
    user.add_order(order)
    assert order in user.get_order_history()


def test_order_to_dict():
    b = Book(1, "B", "A", 10, "Fiction", 1)
    ci = CartItem(b, 2)
    order = Order(1, "x@test.com", [ci], {"address": "123"}, {"method": "card"}, 20)
    result = order.to_dict()
    assert result["order_id"] == 1
    assert result["total_amount"] == 20
    assert result["items"][0]["quantity"] == 2


def test_payment_gateway_success_and_fail():
    good_payment = {"card_number": "1234567890", "payment_method": "card"}
    result = PaymentGateway.process_payment(good_payment)
    assert result["success"] is True
    assert result["transaction_id"]

    bad_payment = {"card_number": "00001111", "payment_method": "card"}
    result = PaymentGateway.process_payment(bad_payment)
    assert result["success"] is False


def test_email_service(monkeypatch):
    called = {}

    def fake_print(*args, **kwargs):
        called["printed"] = True

    monkeypatch.setattr("builtins.print", fake_print)

    b = Book(1, "B", "A", 10, "Fiction", 1)
    ci = CartItem(b, 1)
    order = Order(1, "x@test.com", [ci], {"address": "123"}, {}, 10)

    result = EmailService.send_order_confirmation("x@test.com", order)
    assert result is True
    assert "printed" in called
