import re, subprocess, sys, statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERF = ROOT / "perf"
PERF.mkdir(exist_ok=True)

def run_timeit(n=5):
    times = []
    for _ in range(n):
        subprocess.run([sys.executable, "scripts/timeit_cart.py"], cwd=ROOT, check=False, capture_output=True, text=True)
        txt = (PERF / "timeit_output.txt").read_text(encoding="utf-8")
        m = re.findall(r"over 200 calls: ([0-9.]+)s", txt)
        if m:
            times.append(float(m[-1]))
    return times

def run_profile():
    subprocess.run([sys.executable, "scripts/profile_cart.py"], cwd=ROOT, check=False)

if __name__ == "__main__":
    times = run_timeit(n=5)
    run_profile()
    med = statistics.median(times) if times else None
    with (PERF / "summary.txt").open("w", encoding="utf-8") as f:
        f.write("Performance Summary\n")
        f.write("-------------------\n")
        if med is not None:
            f.write(f"Median timeit (200 calls): {med:.6f}s\n")
        else:
            f.write("Median timeit: N/A\n")
        f.write("See cprofile_top10.txt for profile details.\n")
    print(f"Wrote {PERF/'summary.txt'}")
