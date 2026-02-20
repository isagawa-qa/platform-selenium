# Getting Started

## Prerequisites

- **Python 3.10+**
- **Chrome** or **Brave** browser
- **Claude Code** — [install instructions](https://claude.ai/claude-code)
- **Node.js 18+** (for Playwright MCP server)

## Installation

### 1. Clone and set up

```bash
git clone https://github.com/isagawa-qa/platform.git
cd platform
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env` to set your preferences:

```
BROWSER=chrome        # or 'brave'
HEADLESS=true         # or 'false' for visible browser
TEST_ENV=DEFAULT      # matches key in environment_config.json
```

### 3. Add your test targets

Edit `framework/resources/config/environment_config.json` to add your application URLs:

```json
{
  "DEFAULT": {
    "url": "http://www.automationpractice.pl/index.php"
  },
  "myapp": {
    "url": "https://staging.your-app.com"
  }
}
```

Add credentials to `tests/data/test_users.json` if needed:

```json
{
  "myapp_user": {
    "email": "test@example.com",
    "password": "your-test-password"
  }
}
```

### 4. Run existing tests

```bash
# Run all tests
pytest tests/

# Run with a specific environment
pytest tests/ --env=myapp

# Run in headless mode
pytest tests/ --headless

# Generate HTML report
pytest tests/ --html=report.html
```

## AI-Powered Test Generation

### Setup Claude Code

1. Install Claude Code if you haven't already
2. Open a terminal in the `platform/` directory
3. Run `claude` to start

### Generate your first test

Tell Claude what you want to test:

```
Create a test for the login workflow on https://staging.your-app.com

User: testuser@example.com
Password: testpass123
```

The kernel will discover page elements, generate code following the 5-layer architecture, run the test, and iterate with human-in-the-loop if it fails.

## Windows Users

The `.mcp.json` is configured for cross-platform use with `npx`. If you encounter issues with the Playwright MCP server on Windows, create a `.mcp.json` override:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "cmd",
      "args": ["/c", "npx", "@playwright/mcp@latest"]
    }
  }
}
```

## Next Steps

- Browse `framework/_reference/` for code examples
- Check [CONTRIBUTING.md](../CONTRIBUTING.md) if you want to contribute
