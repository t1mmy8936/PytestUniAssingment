# Performance Pack (timeit + cProfile)

## Usage
```bash
# from repo root
source .venv/bin/activate
export APP_ENV=staging SECRET_KEY=dev_key DISABLE_EMAILS=true

# pytest-based (writes into perf/)
pytest -k "test_cart_total_price_timeit or test_cart_total_price_profile"

# standalone runs (no pytest capture)
python scripts/timeit_cart.py
python scripts/profile_cart.py
python scripts/collect_perf.py

# results
open perf/timeit_output.txt
open perf/cprofile_top10.txt
open perf/summary.txt
