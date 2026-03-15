import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import { spawn } from 'child_process';

// ---------------------------------------------------------------------------
// Regex patterns for Python test discovery
// ---------------------------------------------------------------------------
const RE_TEST_CLASS  = /^class (Test\w+)/;
const RE_TEST_METHOD = /^    def (test_\w+)/;

// Matches pytest verbose output lines:
//   tests/foo/test_bar.py::TestBar::test_baz PASSED                  [ 50%]
//   tests/foo/test_bar.py::TestBar::test_baz FAILED                  [ 50%]
const RE_RESULT = /^(tests\/\S+)\s+(PASSED|FAILED|ERROR)\s/;

// Matches the short-summary section:
//   FAILED tests/foo/test_bar.py::TestBar::test_baz - AssertionError: ...
const RE_SUMMARY = /^(?:FAILED|ERROR)\s+(tests\/\S+)\s+-\s+(.+)$/;

// ---------------------------------------------------------------------------
// Activation
// ---------------------------------------------------------------------------
export function activate(context: vscode.ExtensionContext): void {
  const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
  if (!workspaceRoot) return;

  const ctrl = vscode.tests.createTestController(
    'platformSeleniumTests',
    'Platform Selenium'
  );
  context.subscriptions.push(ctrl);

  // Manual refresh button in the Test Explorer toolbar
  ctrl.refreshHandler = async () => {
    ctrl.items.replace([]);
    await discoverAll(ctrl, workspaceRoot);
  };

  // Watch test files for changes
  const watcher = vscode.workspace.createFileSystemWatcher(
    new vscode.RelativePattern(workspaceRoot, 'tests/**/*.py')
  );
  watcher.onDidCreate(uri => updateFile(ctrl, uri));
  watcher.onDidChange(uri => updateFile(ctrl, uri));
  watcher.onDidDelete(uri => {
    const id = relId(uri.fsPath, workspaceRoot);
    ctrl.items.delete(id);
  });
  context.subscriptions.push(watcher);

  // Run profile (shows a ▶ button next to each test/class/file)
  const runProfile = ctrl.createRunProfile(
    'Run',
    vscode.TestRunProfileKind.Run,
    (request, token) => runHandler(ctrl, request, token, workspaceRoot),
    /* isDefault */ true
  );
  context.subscriptions.push(runProfile);

  // Initial discovery
  discoverAll(ctrl, workspaceRoot);

  // Kernel state status bar
  setupKernelStatusBar(context, workspaceRoot);
}

export function deactivate(): void {}

// ---------------------------------------------------------------------------
// Kernel status bar
// ---------------------------------------------------------------------------

function setupKernelStatusBar(
  context: vscode.ExtensionContext,
  workspaceRoot: string
): void {
  const item = vscode.window.createStatusBarItem(
    vscode.StatusBarAlignment.Right,
    100
  );
  item.command = 'platformSelenium.openKernelState';
  context.subscriptions.push(item);

  // Click → open workflow JSON in editor
  context.subscriptions.push(
    vscode.commands.registerCommand('platformSelenium.openKernelState', () => {
      const domain = readKernelDomain(workspaceRoot);
      const target = domain
        ? path.join(workspaceRoot, '.claude', 'state', `${domain}_workflow.json`)
        : path.join(workspaceRoot, '.claude', 'state', 'session_state.json');
      if (fs.existsSync(target)) {
        vscode.window.showTextDocument(vscode.Uri.file(target));
      }
    })
  );

  // Watch state files for changes (event-driven, no polling)
  const stateWatcher = vscode.workspace.createFileSystemWatcher(
    new vscode.RelativePattern(workspaceRoot, '.claude/state/*.json')
  );
  const refresh = (): void => updateKernelStatusBar(item, workspaceRoot);
  stateWatcher.onDidChange(refresh);
  stateWatcher.onDidCreate(refresh);
  stateWatcher.onDidDelete(refresh);
  context.subscriptions.push(stateWatcher);

  updateKernelStatusBar(item, workspaceRoot);
}

function readJsonSafe(filePath: string): Record<string, unknown> {
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf8')) as Record<string, unknown>;
  } catch {
    return {};
  }
}

function readKernelDomain(workspaceRoot: string): string | undefined {
  const p = path.join(workspaceRoot, '.claude', 'state', 'session_state.json');
  const s = readJsonSafe(p);
  return typeof s.domain === 'string' ? s.domain : undefined;
}

function updateKernelStatusBar(
  item: vscode.StatusBarItem,
  workspaceRoot: string
): void {
  const stateDir    = path.join(workspaceRoot, '.claude', 'state');
  const sessionPath = path.join(stateDir, 'session_state.json');

  if (!fs.existsSync(sessionPath)) {
    item.text = '$(circle-slash) kernel';
    item.tooltip = 'Kernel not started';
    item.backgroundColor = undefined;
    item.show();
    return;
  }

  const session = readJsonSafe(sessionPath);
  const domain  = typeof session.domain === 'string' ? session.domain : undefined;

  if (!domain) {
    item.text = '$(circle-slash) kernel';
    item.tooltip = 'No domain configured';
    item.backgroundColor = undefined;
    item.show();
    return;
  }

  const workflow     = readJsonSafe(path.join(stateDir, `${domain}_workflow.json`));
  const needsLearn   = session.needs_learn === true;
  const anchored     = workflow.anchored === true;
  const actionsSince = typeof workflow.actions_since_anchor === 'number' ? workflow.actions_since_anchor : 0;
  const actionsLimit = typeof workflow.actions_limit        === 'number' ? workflow.actions_limit        : 10;

  item.tooltip = `Kernel: ${domain}\n${actionsSince}/${actionsLimit} actions since anchor\nAnchored: ${anchored}`;

  if (needsLearn) {
    item.text = '$(circle-slash) learn needed';
    item.backgroundColor = new vscode.ThemeColor('statusBarItem.errorBackground');
  } else if (!anchored) {
    item.text = '$(circle-slash) anchor needed';
    item.backgroundColor = new vscode.ThemeColor('statusBarItem.errorBackground');
  } else if (actionsLimit > 0 && actionsSince / actionsLimit >= 0.8) {
    item.text = `$(warning) ${actionsSince}/${actionsLimit}`;
    item.backgroundColor = new vscode.ThemeColor('statusBarItem.warningBackground');
  } else {
    item.text = `$(anchor) ${actionsSince}/${actionsLimit}`;
    item.backgroundColor = undefined;
  }

  item.show();
}

// ---------------------------------------------------------------------------
// Discovery
// ---------------------------------------------------------------------------

function relId(absPath: string, root: string): string {
  return path.relative(root, absPath);
}

async function discoverAll(
  ctrl: vscode.TestController,
  root: string
): Promise<void> {
  const uris = await vscode.workspace.findFiles(
    new vscode.RelativePattern(root, 'tests/**/*.py'),
    '**/conftest.py'
  );
  await Promise.all(uris.map(uri => updateFile(ctrl, uri)));
}

async function updateFile(
  ctrl: vscode.TestController,
  uri: vscode.Uri
): Promise<void> {
  const basename = path.basename(uri.fsPath);
  if (!basename.startsWith('test_') || basename === 'conftest.py') return;

  let src: string;
  try {
    src = fs.readFileSync(uri.fsPath, 'utf8');
  } catch {
    return;
  }

  const root = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath ?? '';
  const fileId = relId(uri.fsPath, root);

  // File-level item (the node shown as the file in the tree)
  const fileItem = ctrl.createTestItem(fileId, basename, uri);
  fileItem.canResolveChildren = true;
  fileItem.children.replace([]);
  ctrl.items.add(fileItem);

  const lines = src.split('\n');
  let currentClass: vscode.TestItem | null = null;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    const classMatch = line.match(RE_TEST_CLASS);
    if (classMatch) {
      const className = classMatch[1];
      const classId   = `${fileId}::${className}`;
      const classItem = ctrl.createTestItem(classId, className, uri);
      classItem.range = new vscode.Range(i, 0, i, line.length);
      fileItem.children.add(classItem);
      currentClass = classItem;
      continue;
    }

    const methodMatch = line.match(RE_TEST_METHOD);
    if (methodMatch && currentClass) {
      const methodName = methodMatch[1];
      const methodId   = `${currentClass.id}::${methodName}`;
      const methodItem = ctrl.createTestItem(methodId, methodName, uri);
      methodItem.range = new vscode.Range(i, 0, i, line.length);
      currentClass.children.add(methodItem);
    }
  }
}

// ---------------------------------------------------------------------------
// Running
// ---------------------------------------------------------------------------

async function runHandler(
  ctrl: vscode.TestController,
  request: vscode.TestRunRequest,
  token: vscode.CancellationToken,
  root: string
): Promise<void> {
  const run = ctrl.createTestRun(request);

  // Collect leaf test items and their pytest node IDs
  const leafItems: vscode.TestItem[] = [];

  function collect(item: vscode.TestItem): void {
    if (request.exclude?.includes(item)) return;
    if (item.children.size === 0) {
      leafItems.push(item);
    } else {
      item.children.forEach(collect);
    }
  }

  if (request.include) {
    request.include.forEach(collect);
  } else {
    ctrl.items.forEach(collect);
  }

  // Mark all as enqueued before starting
  leafItems.forEach(item => run.enqueued(item));

  // Build pytest args
  const config    = vscode.workspace.getConfiguration('platformSelenium');
  const extraArgs = config.get<string[]>('pytestArgs') ?? [];
  const nodeIds   = leafItems.map(i => i.id);
  const args      = [
    '-m', 'pytest',
    ...nodeIds,
    '-v',
    '--tb=short',
    '--no-header',
    '-p', 'no:cacheprovider',
    ...extraArgs,
  ];

  const python = resolvePython(root, config.get<string>('pythonPath'));
  run.appendOutput(`\x1b[36m$ ${python} ${args.join(' ')}\x1b[0m\r\n\r\n`);

  // Mark leaves as started
  leafItems.forEach(item => run.started(item));

  // Spawn pytest
  const proc = spawn(python, args, { cwd: root, env: process.env });
  token.onCancellationRequested(() => proc.kill());

  let stdout = '';
  proc.stdout?.on('data', (chunk: Buffer) => {
    const text = chunk.toString();
    stdout += text;
    run.appendOutput(text.replace(/\n/g, '\r\n'));
  });
  proc.stderr?.on('data', (chunk: Buffer) => {
    run.appendOutput(chunk.toString().replace(/\n/g, '\r\n'));
  });

  await new Promise<void>(resolve => proc.on('close', resolve));

  // Build a map of testId → failure message from the short-summary section
  const failMessages = parseFailureSummary(stdout);

  // Map results back to TestItems
  const itemById = new Map<string, vscode.TestItem>(
    leafItems.map(i => [i.id, i])
  );

  for (const line of stdout.split('\n')) {
    const m = line.match(RE_RESULT);
    if (!m) continue;
    const [, testId, status] = m;
    const item = itemById.get(testId);
    if (!item) continue;

    if (status === 'PASSED') {
      run.passed(item);
    } else {
      const detail  = failMessages.get(testId) ?? 'Test failed';
      const message = new vscode.TestMessage(detail);
      // Point the error at the test method's location for gutter decoration
      if (item.uri && item.range) {
        message.location = new vscode.Location(item.uri, item.range.start);
      }
      run.failed(item, message);
    }

    itemById.delete(testId); // mark as resolved
  }

  // Any item not resolved by output → mark as skipped (e.g. collection error)
  itemById.forEach(item => run.skipped(item));

  run.end();
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/**
 * Parse the "short test summary info" block at the bottom of pytest -v output.
 * Returns a map of testId → error message string.
 */
function parseFailureSummary(output: string): Map<string, string> {
  const map = new Map<string, string>();
  let inSummary = false;

  for (const line of output.split('\n')) {
    if (line.includes('short test summary info')) {
      inSummary = true;
      continue;
    }
    if (!inSummary) continue;
    if (line.startsWith('=')) break; // end of summary section

    const m = line.match(RE_SUMMARY);
    if (m) {
      map.set(m[1], m[2].trim());
    }
  }

  return map;
}

/**
 * Resolve the Python executable to use.
 * Priority: user setting → venv/bin/python → venv/Scripts/python.exe → python3
 */
function resolvePython(root: string, configured?: string): string {
  if (configured && configured.trim()) return configured.trim();

  const candidates = [
    path.join(root, 'venv', 'bin', 'python'),
    path.join(root, 'venv', 'Scripts', 'python.exe'),
    path.join(root, '.venv', 'bin', 'python'),
    path.join(root, '.venv', 'Scripts', 'python.exe'),
  ];

  for (const p of candidates) {
    if (fs.existsSync(p)) return p;
  }

  return 'python3';
}
