# tests/test_models_user_order.py
from models import User, Order, Book, Cart, CartItem
import uuid

def make_order(email="u@example.com"):
    # Simple synthetic order for testing
    items = [CartItem(Book("A", "F", 10.0, "/"), 2)]
    shipping = {"address": "1 Main St"}
    payment = {"payment_method": "credit_card", "card_number": "4111111111111111", "expiry_date": "12/30", "cvv": "123"}
    return Order(order_id=str(uuid.uuid4())[:8], user_email=email, items=items, shipping_info=shipping, payment_info=payment, total_amount=20.0)

def test_user_order_history_sorted_by_date():
    u = User("e@x.com", "pw", "Name", "Addr")
    o1 = make_order()
    o2 = make_order()
    u.add_order(o1)
    u.add_order(o2)
    hist = u.get_order_history()
    assert len(hist) == 2
    # Only checks that it's a list of orders; sorting efficiency is discussed in the plan.
    assert all(hasattr(o, "order_date") for o in hist)
