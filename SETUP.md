# Setup Guide — platform-selenium

Get this framework running against your application in one session.

---

## Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| Python | 3.10+ | https://python.org/downloads |
| Google Chrome | Latest | https://google.com/chrome |
| Git | Any | https://git-scm.com/downloads |

ChromeDriver is installed automatically by `webdriver-manager` — you do not need to install it manually.

---

## Step 1: Clone

```bash
git clone https://github.com/isagawa-qa/platform-selenium.git
cd platform-selenium
```

---

## Step 2: Python Environment

```bash
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

---

## Step 3: Register Your App

Add your application to `framework/resources/config/environment_config.json`:

```json
{
  "yourapp": {
    "url": "http://localhost:PORT",
    "explicit_wait": 10,
    "screenshots_on_failure": true,
    "screenshot_dir": "screenshots/yourapp"
  }
}
```

The key (`yourapp`) becomes the `--env` flag value when running tests.

---

## Step 4: Verify Setup

Run the smoke test against the default demo environment (no app required):

```bash
pytest tests/navigation/ --env=DEFAULT -v --headless
```

Expected: at least one test collected and run without import errors.

---

## Step 5: Run Tests for Your App

```bash
# Your app must be running first
pytest tests/yourapp/ --env=yourapp -v
pytest tests/yourapp/ --env=yourapp --headless -v
```

---

## Next Steps

| Goal | Read |
|------|------|
| Understand the full workflow | `DEVELOPER_GUIDE.md` |
| Use this framework from a different project | `INTEGRATION.md` |
| Generate tests with AI | Open Claude Code here, then `/qa-workflow` |

---

## Troubleshooting

**`ModuleNotFoundError`** — virtual env not activated. Run `source .venv/bin/activate` first.

**`WebDriverException: ChromeDriver not found`** — first run downloads ChromeDriver automatically. Ensure you have internet access and Chrome installed.

**`ValueError: No environment match found`** — your env key is not in `environment_config.json`. Add it per Step 3.

**Tests blocked by hook** — if you see `BLOCKED:` in the terminal, invoke the command shown (e.g. `/kernel/anchor`). This is the kernel enforcement system working correctly.
