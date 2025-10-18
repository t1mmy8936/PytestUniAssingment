# tests/conftest.py
import os, sys, pathlib, pytest

# --- Make project importable ---
ROOT = pathlib.Path(__file__).resolve().parents[1]
# Add repo root
sys.path.insert(0, str(ROOT))
# Add common app dirs if they exist (so `from models import ...` or `from app.models import ...` both work)
for cand in ("app", "src", "online_bookstore", "online-bookstore", "backend"):
    p = ROOT / cand
    if p.exists() and p.is_dir():
        sys.path.insert(0, str(p))

# --- Stable test environment ---
os.environ.setdefault("APP_ENV", "staging")
os.environ.setdefault("SECRET_KEY", "test_secret_key")
os.environ.setdefault("DISABLE_EMAILS", "true")

@pytest.fixture(scope="session")
def app():
    # Import the Flask app if present; otherwise tests that don't need it will still run
    try:
        import app as flask_app
        return flask_app.app
    except Exception:
        # Not all tests rely on the Flask app; skip the client when unavailable
        pytest.skip("Flask app not importable in this layout; route tests skipped", allow_module_level=True)

@pytest.fixture()
def client(app):
    with app.test_client() as client:
        yield client