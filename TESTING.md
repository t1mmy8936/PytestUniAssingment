# Testing & CI Guide

## Quick Start
1. Create a virtual environment and install:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-test.txt
   cp .env.staging .env
   ```
2. Run tests:
   ```bash
   pytest
   ```

## Environments
- Copy one of the provided files:
  - `.env.staging` for local dev
  - `.env.production` for prod-like runs
- Config keys:
  - `APP_ENV`: `staging` or `production`
  - `SECRET_KEY`: Flask secret, used by sessions
  - `DISABLE_EMAILS`: When `true`, email sending is mocked/no-op

## CI/CD
- A GitHub Actions workflow runs tests on every push/PR.
- Coverage is printed to the job logs. You can later upload XML to Codecov if desired.

## What the tests cover
- **Unit**: cart operations, user/order basics
- **Integration**: homepage, add-to-cart invalid input handling, checkout discount code behavior
- **Performance (informational)**: `Cart.get_total_price()` via `timeit` and `cProfile`

## Known Bugs Exposed by Tests
- `Cart.update_quantity()` does not remove an item for `quantity <= 0` (marked `@pytest.mark.xfail_bug`).
- `add-to-cart` casts quantity with `int(...)` without error handling, which may 500 on bad input.
- Discount code handling is case sensitive.

## Suggested Improvements (Prioritized)
1. **Input validation** (routes: `add_to_cart`, `update_cart`, checkout): wrap `int(...)` in try/except, clamp to `[0, max]`, and surface user-friendly messages.
2. **Cart semantics**: In `update_quantity`, remove the line item when `quantity <= 0`; validate non-negative integers only.
3. **Discount codes**: Normalize to lower-case before comparison and trim spaces; consider a dict of codes and % values.
4. **Performance**: Replace the nested loop in `Cart.get_total_price()` with `total += item.book.price * item.quantity` (reduces complexity and profiler hot spot).
5. **Payment validation**: Validate card lengths/Luhn, expiry format and CVV, and add a PayPal branch; tests can be added as you implement.
6. **Order management**: Avoid sorting the entire list on every insert; maintain append-only and sort on demand or keep a sorted invariant efficiently.
7. **Config adoption**: In `app.py`, read `SECRET_KEY` and environment toggles from `config.py` to avoid hardcoded secrets.

## Extending Tests
- Add route tests for login/logout, profile update, and checkout required fields.
- Add property-based tests for cart quantities (e.g., `hypothesis`).
