import os, sys, timeit
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for cand in (ROOT, ROOT / "app", ROOT / "src"):
    s = str(cand)
    if s not in sys.path: sys.path.insert(0, s)

try:
    from models import Book, Cart
except ModuleNotFoundError:
    from app.models import Book, Cart  # type: ignore

def setup_cart():
    cart = Cart()
    for i in range(200):
        cart.add_book(Book(f"B{i}", "C", 1.0 + (i % 5), "/"), (i % 7) + 1)
    return cart

def bench():
    cart = setup_cart()
    return cart.get_total_price()

if __name__ == "__main__":
    t = timeit.timeit(bench, number=200)
    out_dir = ROOT / "perf"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "timeit_output.txt"
    with out_path.open("a", encoding="utf-8") as f:
        f.write(f"[timeit] Cart.get_total_price() over 200 calls: {t:.6f}s\n")
    print(f"Wrote {out_path}")
