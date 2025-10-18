# Online Bookstore – Setup & Testing Guide

This project includes an online bookstore app plus a full testing and CI setup.

---

## 0) Prerequisites

- **Python 3.10+** (3.11/3.12/3.13 all fine)
- **pip** package manager (comes with Python)
- **Git**
- **macOS/Homebrew users**: strongly recommended to use a virtual environment (PEP 668 prevents system-wide installs)

---

## 1) First-Time Setup

1. **Unpack the testing pack (if provided)**
   ```zsh
   unzip ~/Downloads/online-bookstore-testing-pack.zip -d .
   rsync -av online-bookstore-testing-additions/ ./
   ```

2. **Create and activate a virtual environment**
   ```zsh
   python3 -m venv .venv
   source .venv/bin/activate

   # Optional: upgrade pip inside the venv
   python -m pip install --upgrade pip
   ```

3. **Install dependencies**
   ```zsh
   pip install -r requirements.txt
   pip install -r requirements-test.txt
   ```

   > Optional: merge the small patch into your main requirements:
   > ```zsh
   > patch -p1 < requirements.patch
   > ```

---

## 2) Environment Setup

Copy one of the sample environment files:

```zsh
cp .env.staging .env
```

- `APP_ENV` – `staging` (default) or `production`
- `SECRET_KEY` – set a strong key for production
- `DISABLE_EMAILS` – `true` in staging to prevent email sending

Configuration is loaded via [`config.py`](./config.py) (using `python-dotenv`).

---

## 3) Running the Tests

Run from the repo root:

```zsh
export APP_ENV=staging SECRET_KEY=dev_key DISABLE_EMAILS=true
pytest
```

Useful subsets:

```zsh
pytest -m "not integration"      # unit tests only
pytest -m integration            # integration tests
pytest --cov=. --cov-report=term-missing
```

---

## 4) Running the App

If your entrypoint is `app.py` with a Flask instance `app`:

```zsh
export FLASK_APP=app:app
flask run
```

Make sure `app.py` loads config:

```python
from config import get_config

app.config.from_object(get_config())
app.secret_key = app.config["SECRET_KEY"]
```

---

## 5) CI/CD

- GitHub Actions workflow is in `.github/workflows/ci.yml`
- On every push/PR:
  - Installs dependencies
  - Runs `pytest` with coverage
- You can add a coverage gate by updating the workflow:
  ```yaml
  pytest --cov=. --cov-report=term-missing --cov-fail-under=75
  ```

---

## 6) Known Bugs Exposed by Tests

- **Cart**: `update_quantity` does not remove an item when quantity `<= 0`
- **Add-to-cart route**: invalid quantity (`"abc"`) can crash instead of showing a friendly message
- **Discount codes**: case sensitive (e.g. `"save10"` not accepted, only `"SAVE10"`)

These are marked with `@pytest.mark.xfail_bug` so CI passes but issues remain visible.

---

## 7) Suggested Improvements

- Input validation (quantity, checkout form fields)
- Fix `Cart.update_quantity` to remove items when `<= 0`
- Normalize discount codes (`.strip().lower()`)
- Optimize `Cart.get_total_price()` with direct multiplication
- Add payment validation (card number, expiry, CVV, PayPal option)
- Add coverage threshold in CI

---

## 8) Troubleshooting

**PEP 668 / "externally-managed-environment"**  
Always use a virtual environment (`python3 -m venv .venv`).

**Module import errors (`No module named 'models'`)**  
- Run `pytest` from the repo root
- `tests/conftest.py` tries to fix `sys.path` for common layouts
- As fallback:  
  ```zsh
  export PYTHONPATH="$(pwd):$(pwd)/app:$(pwd)/src"
  pytest
  ```

---

