import os, io, timeit, cProfile, pstats
from pathlib import Path

def _import_models():
    import sys, importlib
    REPO = Path.cwd()
    for cand in (REPO, REPO / "app", REPO / "src"):
        s = str(cand)
        if s not in sys.path: sys.path.insert(0, s)
    try:
        return importlib.import_module("models")
    except ModuleNotFoundError:
        return importlib.import_module("app.models")

models = _import_models()
Book = models.Book
Cart = models.Cart

PERF_DIR = Path("perf")
PERF_DIR.mkdir(exist_ok=True)

def _build_cart_timeit():
    cart = Cart()
    for i in range(200):
        cart.add_book(Book(f"B{i}", "C", 1.0 + (i % 5), "/"), (i % 7) + 1)
    return cart

def _build_cart_profile():
    cart = Cart()
    for i in range(500):
        cart.add_book(Book(f"B{i}", "C", 1.0 + (i % 5), "/"), (i % 10) + 1)
    return cart

def test_cart_total_price_timeit():
    cart = _build_cart_timeit()
    t = timeit.timeit(lambda: cart.get_total_price(), number=200)
    with open(PERF_DIR / "timeit_output.txt", "a", encoding="utf-8") as f:
        f.write(f"[timeit] Cart.get_total_price() over 200 calls: {t:.6f}s\n")

def test_cart_total_price_profile():
    cart = _build_cart_profile()
    pr = cProfile.Profile()
    pr.enable()
    _ = cart.get_total_price()
    pr.disable()
    s = io.StringIO()
    pstats.Stats(pr, stream=s).strip_dirs().sort_stats("cumtime").print_stats(15)
    with open(PERF_DIR / "cprofile_top10.txt", "w", encoding="utf-8") as f:
        f.write(s.getvalue())
