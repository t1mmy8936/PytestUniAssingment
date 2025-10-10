# tests/test_performance.py
# These are informative tests: they don't assert on timing (flaky in CI),
# but they print profiling output to help you quantify inefficiencies.
import timeit
import cProfile, pstats, io
from models import Book, Cart

def test_cart_total_price_timeit(capsys):
    cart = Cart()
    for i in range(200):
        cart.add_book(Book(f"B{i}", "C", 1.0 + (i % 5), "/"), (i % 7) + 1)
    # Measure the current implementation
    t = timeit.timeit(lambda: cart.get_total_price(), number=200)
    print(f"[timeit] Cart.get_total_price() over 200 calls: {t:.4f}s")
    # Emit captured output to pytest logs
    captured = capsys.readouterr()

def test_cart_total_price_profile(capsys):
    cart = Cart()
    for i in range(500):
        cart.add_book(Book(f"B{i}", "C", 1.0 + (i % 5), "/"), (i % 10) + 1)
    pr = cProfile.Profile()
    pr.enable()
    _ = cart.get_total_price()
    pr.disable()
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats("cumtime")
    ps.print_stats(10)
    print(s.getvalue())
    captured = capsys.readouterr()
