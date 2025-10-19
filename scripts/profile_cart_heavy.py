# scripts/profile_cart_heavy.py
import os, sys, io, cProfile, pstats, math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for cand in (ROOT, ROOT / "app", ROOT / "src"):
    s = str(cand)
    if s not in sys.path:
        sys.path.insert(0, s)

# Adjust import path if your models live elsewhere
try:
    from models import Book, Cart
except ModuleNotFoundError:
    from app.models import Book, Cart  # type: ignore

def build_cart(n_items=5000, max_qty=20):
    cart = Cart()
    for i in range(n_items):
        price = 1.0 + (i % 7)  # vary price a bit
        qty = 1 + (i % max_qty)
        cart.add_book(Book(f"B{i}", "Category", price, "/img"), qty)
    return cart

def main():
    cart = build_cart()
    pr = cProfile.Profile()
    pr.enable()

    # Profile a LOT of repeated calls so the profiler has real time to attribute
    for _ in range(2000):        # increase if still too fast
        _ = cart.get_total_price()

    pr.disable()

    out_dir = ROOT / "perf"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "cprofile_top10.txt"

    s = io.StringIO()
    # Sort by cumulative time, print more lines so you can see genexpr/sum, etc.
    pstats.Stats(pr, stream=s).strip_dirs().sort_stats("cumtime").print_stats(30)
    out_path.write_text(s.getvalue(), encoding="utf-8")
    print(f"Wrote {out_path}")

if __name__ == "__main__":
    main()
