# Step 2: Discover Repo Structure

Scan and list what exists:

```
SCAN:
├── framework/
│   ├── _reference/          → Code pattern examples
│   ├── interfaces/          → Infrastructure layer
│   └── resources/           → Utilities, config, drivers
├── .claude/
│   ├── skills/              → Workflow protocols
│   └── commands/            → Entry points (non-kernel)
├── tests/
│   ├── conftest.py          → Pytest fixtures
│   └── data/                → Test data
```

## Action

List all files found in each location.

## Output

Report file counts per directory.
