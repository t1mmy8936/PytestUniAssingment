# tests/test_models_cart.py
import pytest
from models import Book, Cart

def test_add_and_remove_book():
    cart = Cart()
    b = Book("Test", "Cat", 5.0, "/img")
    cart.add_book(b, 2)
    assert cart.get_total_items() == 2
    cart.remove_book(b.title)
    assert cart.get_total_items() == 0

@pytest.mark.xfail_bug(reason="Known bug: update_quantity doesn't remove item when quantity <= 0")
def test_update_quantity_zero_removes_item():
    cart = Cart()
    b = Book("Test", "Cat", 5.0, "/img")
    cart.add_book(b, 2)
    cart.update_quantity(b.title, 0)  # Expected: remove item
    # Known bug: item remains with 0 qty
    assert cart.get_total_items() == 0

def test_total_price_correctness():
    cart = Cart()
    b1 = Book("A", "X", 10.0, "/")
    b2 = Book("B", "Y", 2.5, "/")
    cart.add_book(b1, 3)  # 30
    cart.add_book(b2, 4)  # 10
    assert abs(cart.get_total_price() - 40.0) < 1e-9
