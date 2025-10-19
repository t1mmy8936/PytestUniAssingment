# scripts/profile_cart.py
import cProfile, pstats, io, os, sys

# --- Make local imports robust ---
ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, os.pardir))
for cand in (REPO, os.path.join(REPO, "app"), os.path.join(REPO, "src")):
    if cand not in sys.path:
        sys.path.insert(0, cand)

from models import Book, Cart  # adjust if your models are under app.models

def build_cart(n=500):
    cart = Cart()
    for i in range(n):
        cart.add_book(Book(f"B{i}", "C", 1.0 + (i % 5), "/"), (i % 10) + 1)
    return cart

def main():
    cart = build_cart()
    pr = cProfile.Profile()
    pr.enable()
    _ = cart.get_total_price()
    pr.disable()

    os.makedirs("perf", exist_ok=True)
    out_path = os.path.join("perf", "cprofile_top10.txt")
    s = io.StringIO()
    pstats.Stats(pr, stream=s).strip_dirs().sort_stats("cumtime").print_stats(15)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(s.getvalue())
    print(f"Wrote {out_path}")

if __name__ == "__main__":
    main()
import os, sys, io, cProfile, pstats
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for cand in (ROOT, ROOT / "app", ROOT / "src"):
    s = str(cand)
    if s not in sys.path: sys.path.insert(0, s)

try:
    from models import Book, Cart
except ModuleNotFoundError:
    from app.models import Book, Cart  # type: ignore

def build_cart(n=500):
    cart = Cart()
    for i in range(n):
        cart.add_book(Book(f"B{i}", "C", 1.0 + (i % 5), "/"), (i % 10) + 1)
    return cart

def main():
    cart = build_cart()
    pr = cProfile.Profile()
    pr.enable()
    _ = cart.get_total_price()
    pr.disable()

    out_dir = ROOT / "perf"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "cprofile_top10.txt"
    s = io.StringIO()
    pstats.Stats(pr, stream=s).strip_dirs().sort_stats("cumtime").print_stats(15)
    out_path.write_text(s.getvalue(), encoding="utf-8")
    print(f"Wrote {out_path}")

if __name__ == "__main__":
    main()
