# Step 1: Prerequisites

Before domain setup, verify all dependencies are installed and configured.

## MCP Servers

### Playwright MCP (Required)

Check if configured in `.claude/mcp.json`:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp"]
    }
  }
}
```

**If not configured:**
1. Create/update `.claude/mcp.json` with above config
2. Set restart state (see below)
3. Stop and wait for restart

### QA Automation MCP (If applicable)

Check if configured:

```json
{
  "mcpServers": {
    "qa-automation": {
      "command": "python",
      "args": ["server.py"],
      "cwd": "./mcp_server"
    }
  }
}
```

## Python Dependencies

Check `requirements.txt` exists and install:

```bash
pip install -r requirements.txt
```

### Required packages:
- selenium
- pytest
- pytest-html
- webdriver-manager
- faker

## Browser Driver

Verify ChromeDriver or use webdriver-manager:

```python
# framework/resources/chromedriver/driver.py should handle this
from webdriver_manager.chrome import ChromeDriverManager
```

## Settings

Verify `.claude/settings.local.json` has MCP servers enabled:

```json
{
  "enableAllProjectMcpServers": true
}
```

## Checklist

| Dependency | Check | Action if Missing |
|------------|-------|-------------------|
| Playwright MCP | `.claude/mcp.json` has playwright | Add config → restart |
| Python deps | `pip list` shows selenium, pytest | `pip install -r requirements.txt` |
| Browser driver | ChromeDriver accessible | webdriver-manager handles this |
| MCP enabled | settings.local.json configured | Add enableAllProjectMcpServers |

---

## Restart Flow (Integration with Session-Start Loop)

If ANY MCP configuration changed, restart is required. MCP servers load at Claude Code startup.

### Step 1a: Set Restart State

Create/update `.claude/state/session_state.json`:

```json
{
  "session_started": true,
  "domain": "qa",
  "needs_restart": true,
  "resume_after_restart": "domain-setup",
  "resume_step": 2,
  "timestamp": "[ISO-8601]"
}
```

### Step 1b: Report and Stop

```
PREREQUISITES: Restart Required

Changed:
- [list what was configured/changed]

State saved. After restart, domain-setup will resume from Step 2.

⚠️  RESTART REQUIRED

1. Restart Claude Code now
2. Say "continue"
3. /kernel/session-start will read state and resume

Waiting for restart...
```

**STOP. Do not proceed until user restarts.**

### Step 1c: After Restart (Handled by session-start)

When user says "continue":
1. `/kernel/session-start` reads state
2. Sees `needs_restart: true` → clears flag
3. Sees `resume_after_restart: "domain-setup"`
4. Invokes `/kernel/domain-setup`
5. Domain-setup sees `resume_step: 2` → skips to Step 2

---

## No Restart Needed

If all dependencies already configured:

```
PREREQUISITES: All configured

✓ Playwright MCP configured
✓ Python dependencies installed
✓ Browser driver available
✓ MCP enabled in settings

Proceeding to Step 2...
```

Continue to Step 2 immediately.
