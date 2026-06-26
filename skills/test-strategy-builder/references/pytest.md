# pytest codegen patterns (unit + integration)

Loaded when the user names **pytest** (or Python) as the target framework for unit
or integration cases. Turn the Phase B case table into runnable `test_*.py` files
following the patterns below. Patterns are generic — login is used only as a worked
example. Identify the system-under-test and its risk areas first; the table drives
the code.

## File layout

```
<suite>/
├── src/<module>.py        # the system-under-test (real code, or a mock if none exists yet)
├── tests/conftest.py      # shared fixtures (seeded state)
├── tests/test_unit.py     # pure-logic cases
├── tests/test_integration.py  # boundary cases
└── pytest.ini             # pythonpath so `src` imports resolve
```

`pytest.ini`:

```ini
[pytest]
pythonpath = .
testpaths = tests
```

## Case row → test function

Map one table row to one test function. Name it `test_<id>_<slug>` so the file reads
back against the table.

| Table column | Goes to |
|--------------|---------|
| ID + Title | function name `test_u01_email_validator_accepts_valid` |
| Preconditions | fixture or in-body setup |
| Steps / Inputs | the call under test |
| Expected result | the `assert` |

```python
# U-01 Email format validator accepts valid
def test_u01_email_validator_accepts_valid():
    assert validate_email("a@b.com") is True
```

Collapse a row that lists several inputs into one `parametrize`d test:

```python
# U-02 Email validator rejects malformed
@pytest.mark.parametrize("bad", ["a@", "a b@c.com", "", "no-at-sign"])
def test_u02_email_validator_rejects_malformed(bad):
    assert validate_email(bad) is False
```

## Fixtures (conftest.py)

Put shared preconditions in fixtures. Seed the minimum state a case needs.

```python
import pytest
from src.auth import AuthAPI

VALID_EMAIL = "user@example.com"
VALID_PASSWORD = "Pass123!"

@pytest.fixture
def api():
    a = AuthAPI()
    a.register(VALID_EMAIL, VALID_PASSWORD, verified=True)
    return a

@pytest.fixture
def session_token(api):
    status, body = api.login(VALID_EMAIL, VALID_PASSWORD)
    assert status == 200
    return body["token"]
```

## Integration without a live server: the (status, body) boundary

When there is no running HTTP service, model the integration boundary as a small
in-memory object whose methods return `(status_code, body)` tuples. This lets
integration cases assert real status codes and error shapes without a server, and
keeps the cases honest about the contract.

```python
# I-03 Login unknown email -> generic 401 (no user-exists leak)
def test_i03_login_unknown_email(api):
    status, body = api.login("nobody@example.com", VALID_PASSWORD)
    assert status == 401
    assert body["error"] == "invalid_credentials"  # identical to wrong-password
```

When a real service exists, swap the mock call for the project's HTTP client
(`httpx`, `requests`, framework test client) — the assert structure is unchanged.

## Tooling

Recommend, do not auto-install:

```bash
pip install -r requirements.txt   # pytest>=8
pytest
```

## Coverage discipline

- One row → one test (or one parametrized test for an input set).
- Every test asserts the expected result explicitly — no bare "it ran".
- Cover the happy path plus at least one negative/edge per requirement, matching the table.
- After generating, read the tests back against the strategy's risk areas.
