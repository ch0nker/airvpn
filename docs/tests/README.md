# Test Documentation

The project's test runner is a small custom framework (`test/__main__.py`) that dynamically loads each file under `test/units/` as a "unit," runs every function registered with `@test.unit`, and reports pass/fail results with colored output.

### Don't print secrets or config contents

Test output (including `print`/`warn` calls) may end up in CI logs, which are visible to anyone if the repository is public. Never print:

- The raw `API_KEY` value, or any partial/sliced/encoded version of it
- Generated VPN config contents (e.g. a `Config`'s `buffer` or `read()` output), since these can contain embedded keys or credentials that are just as sensitive as the API key itself
- Full request/response objects that might carry the key in a URL or header (e.g. `response.url`, `response.request.headers`)

If you need debug output to diagnose a failing test, prefer non-sensitive signals instead — status codes, presence/absence of a field, or lengths (e.g. `len(config)`):

```py
print(f"Got {len(configs)} configs")   # fine
print(configs[0].read())               # don't — may contain embedded secrets
```

CI automatically masks any log output that exactly matches a configured secret's value, but this isn't a substitute for care — masking won't catch a transformed, partial, or re-encoded copy of the secret.

## Setup

Install the test-specific dependencies before running anything:

```bash
pip install -r test-requirements.txt
```

This installs packages the tests need (like `colorama` and `python-dotenv`) that aren't required by the library itself, so they're kept separate from `requirements.txt`.

You'll also need a `.env` file in the project root with your `API_KEY` set, since most units authenticate against the real API:

```
API_KEY=your_api_key_here
```

See `.env.example` for the expected format.

## Running tests

Run every unit:

```bash
python test
```

Run a single unit by name (matches the filename without `.py`):

```bash
python test userinfo
```

Exit code is `0` if everything passed, `1` if any test raised an exception or returned a string.

## Running tests in CI (GitHub Actions)

The `Run Tests` workflow runs the same suite as `python test`, but it can't read your local `.env` file — it needs its own copy of the API key stored as a GitHub Actions secret named `AIRVPN_API_KEY`, which the workflow passes into the run as the `API_KEY` environment variable:

```yaml
- name: Run tests
  env:
    API_KEY: ${{ secrets.AIRVPN_API_KEY }}
  run: python test
```

### Setting the secret

1. Go to the repository on GitHub.
2. Open **Settings** (repo settings, not your account settings).
3. In the sidebar, go to **Secrets and variables → Actions**.
4. Under the **Secrets** tab, click **New repository secret**.
5. Set:
   - **Name:** `AIRVPN_API_KEY`
   - **Secret:** your AirVPN API key
6. Click **Add secret**.

Only users with admin access to the repository can view or edit this page — the secret's value is never shown again after saving, and it's masked automatically in any workflow log output.

If you're testing from a fork, note that GitHub does not pass repository secrets to workflows triggered from forks by default, for security reasons. Maintainers running the workflow from the base repository (or via `workflow_dispatch`) will have access as normal.

## Writing a unit

Each file under `test/units/` is one unit. A unit registers one or more test functions with the `@test.unit` decorator. `test` is injected automatically by the runner — you don't need to import it.

```py
# test/units/userinfo.py
import os

from airvpn import AirVPN

api = AirVPN(os.getenv("API_KEY"))
userinfo = None

@test.unit
def check_request():
    global userinfo
    userinfo = api.userinfo
```

### Pass / fail behavior

A test function passes if it returns normally (or returns anything that isn't a `str`). It's recorded as a failure in two ways:

| Behavior | Result |
|---|---|
| Raises any `Exception` | Failure — full traceback captured automatically and printed. |
| Returns a `str` | Failure — the returned string is used as the error message. |
| Returns anything else (or nothing) | Success. |

In most cases you don't need a `try`/`except` in your own test — just let exceptions raise naturally and the runner will catch and report them with a full traceback. Only return a string explicitly if you want a custom, human-readable failure message instead of a raw traceback.

```py
@test.unit
def check_user_present():
    if not userinfo.user:
        return "Expected a user value but got None"
```

### Sharing state between test functions in the same unit

Since all test functions in a unit run inside the same module, ordinary module-level variables (like `userinfo` above) can be set in one test and read in another — `@test.unit` functions in the same file run top-to-bottom in the order they're defined.

```py
@test.unit
def check_request():
    global userinfo
    userinfo = api.userinfo

@test.unit
def check_login():
    assert userinfo.user is not None, "Failed to get user"
```

## Environment variables

`.env` (project root) is loaded automatically before any units run, and again before each individual unit — so `os.getenv("API_KEY")` and similar calls work the same way they would in your normal application code.

## Logging inside a unit

Every unit automatically gets two extra functions injected alongside `print` — `print` itself is overridden with a timestamped, color-coded version, and `warn` is added for warning-level output. Neither needs to be imported; the runner injects them into your unit's module before it executes.

```py
print("Fetched userinfo successfully")
warn("Rate limit is getting close")
```

Output looks like:

```
[ 2026-07-17 14:32:07  userinfo  | INFO >  Fetched userinfo successfully
[ 2026-07-17 14:32:08  userinfo  | WARNING >  Rate limit is getting close
```

Both accept the same signature as the built-in `print` (`sep`, `end`, `file`, `flush`), so existing calls to `print(...)` in a unit work without any changes.

## Adding a new unit

1. Create a new file under `test/units/`, e.g. `test/units/devices.py`.
2. Import whatever you need from `airvpn` and set up any module-level state.
3. Register one or more functions with `@test.unit`.
4. Run it directly to confirm it works: `python test.py devices`.

No registration elsewhere is required — `list_units()` automatically discovers every `.py` file in `test/units/`.