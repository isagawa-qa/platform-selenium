"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = __importStar(require("vscode"));
const path = __importStar(require("path"));
const fs = __importStar(require("fs"));
const child_process_1 = require("child_process");
// ---------------------------------------------------------------------------
// Regex patterns for Python test discovery
// ---------------------------------------------------------------------------
const RE_TEST_CLASS = /^class (Test\w+)/;
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
function activate(context) {
    const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
    if (!workspaceRoot)
        return;
    const ctrl = vscode.tests.createTestController('platformSeleniumTests', 'Platform Selenium');
    context.subscriptions.push(ctrl);
    // Manual refresh button in the Test Explorer toolbar
    ctrl.refreshHandler = async () => {
        ctrl.items.replace([]);
        await discoverAll(ctrl, workspaceRoot);
    };
    // Watch test files for changes
    const watcher = vscode.workspace.createFileSystemWatcher(new vscode.RelativePattern(workspaceRoot, 'tests/**/*.py'));
    watcher.onDidCreate(uri => updateFile(ctrl, uri));
    watcher.onDidChange(uri => updateFile(ctrl, uri));
    watcher.onDidDelete(uri => {
        const id = relId(uri.fsPath, workspaceRoot);
        ctrl.items.delete(id);
    });
    context.subscriptions.push(watcher);
    // Run profile (shows a ▶ button next to each test/class/file)
    const runProfile = ctrl.createRunProfile('Run', vscode.TestRunProfileKind.Run, (request, token) => runHandler(ctrl, request, token, workspaceRoot), 
    /* isDefault */ true);
    context.subscriptions.push(runProfile);
    // Initial discovery
    discoverAll(ctrl, workspaceRoot);
    // Kernel state status bar
    setupKernelStatusBar(context, workspaceRoot);
    // Mission Control webview
    context.subscriptions.push(vscode.commands.registerCommand('platformSelenium.openMissionControl', () => {
        MissionControlPanel.createOrShow(workspaceRoot);
    }));
}
function deactivate() { }
// ---------------------------------------------------------------------------
// Kernel status bar
// ---------------------------------------------------------------------------
function setupKernelStatusBar(context, workspaceRoot) {
    const item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    item.command = 'platformSelenium.openKernelState';
    context.subscriptions.push(item);
    // Click → open workflow JSON in editor
    context.subscriptions.push(vscode.commands.registerCommand('platformSelenium.openKernelState', () => {
        const domain = readKernelDomain(workspaceRoot);
        const target = domain
            ? path.join(workspaceRoot, '.claude', 'state', `${domain}_workflow.json`)
            : path.join(workspaceRoot, '.claude', 'state', 'session_state.json');
        if (fs.existsSync(target)) {
            vscode.window.showTextDocument(vscode.Uri.file(target));
        }
    }));
    // Watch state files for changes (event-driven, no polling)
    const stateWatcher = vscode.workspace.createFileSystemWatcher(new vscode.RelativePattern(workspaceRoot, '.claude/state/*.json'));
    const refresh = () => updateKernelStatusBar(item, workspaceRoot);
    stateWatcher.onDidChange(refresh);
    stateWatcher.onDidCreate(refresh);
    stateWatcher.onDidDelete(refresh);
    context.subscriptions.push(stateWatcher);
    updateKernelStatusBar(item, workspaceRoot);
}
function readJsonSafe(filePath) {
    try {
        return JSON.parse(fs.readFileSync(filePath, 'utf8'));
    }
    catch {
        return {};
    }
}
function readKernelDomain(workspaceRoot) {
    const p = path.join(workspaceRoot, '.claude', 'state', 'session_state.json');
    const s = readJsonSafe(p);
    return typeof s.domain === 'string' ? s.domain : undefined;
}
function updateKernelStatusBar(item, workspaceRoot) {
    const stateDir = path.join(workspaceRoot, '.claude', 'state');
    const sessionPath = path.join(stateDir, 'session_state.json');
    if (!fs.existsSync(sessionPath)) {
        item.text = '$(circle-slash) kernel';
        item.tooltip = 'Kernel not started';
        item.backgroundColor = undefined;
        item.show();
        return;
    }
    const session = readJsonSafe(sessionPath);
    const domain = typeof session.domain === 'string' ? session.domain : undefined;
    if (!domain) {
        item.text = '$(circle-slash) kernel';
        item.tooltip = 'No domain configured';
        item.backgroundColor = undefined;
        item.show();
        return;
    }
    const workflow = readJsonSafe(path.join(stateDir, `${domain}_workflow.json`));
    const needsLearn = session.needs_learn === true;
    const anchored = workflow.anchored === true;
    const actionsSince = typeof workflow.actions_since_anchor === 'number' ? workflow.actions_since_anchor : 0;
    const actionsLimit = typeof workflow.actions_limit === 'number' ? workflow.actions_limit : 10;
    item.tooltip = `Kernel: ${domain}\n${actionsSince}/${actionsLimit} actions since anchor\nAnchored: ${anchored}`;
    if (needsLearn) {
        item.text = '$(circle-slash) learn needed';
        item.backgroundColor = new vscode.ThemeColor('statusBarItem.errorBackground');
    }
    else if (!anchored) {
        item.text = '$(circle-slash) anchor needed';
        item.backgroundColor = new vscode.ThemeColor('statusBarItem.errorBackground');
    }
    else if (actionsLimit > 0 && actionsSince / actionsLimit >= 0.8) {
        item.text = `$(warning) ${actionsSince}/${actionsLimit}`;
        item.backgroundColor = new vscode.ThemeColor('statusBarItem.warningBackground');
    }
    else {
        item.text = `$(anchor) ${actionsSince}/${actionsLimit}`;
        item.backgroundColor = undefined;
    }
    item.show();
}
// ---------------------------------------------------------------------------
// Mission Control webview
// ---------------------------------------------------------------------------
class MissionControlPanel {
    static createOrShow(workspaceRoot) {
        const column = vscode.window.activeTextEditor
            ? vscode.window.activeTextEditor.viewColumn
            : undefined;
        if (MissionControlPanel.currentPanel) {
            MissionControlPanel.currentPanel._panel.reveal(column);
            return;
        }
        const panel = vscode.window.createWebviewPanel('missionControl', 'Mission Control', column ?? vscode.ViewColumn.One, { enableScripts: true });
        MissionControlPanel.currentPanel = new MissionControlPanel(panel, workspaceRoot);
    }
    constructor(panel, workspaceRoot) {
        this._disposables = [];
        this._eventLineCount = 0;
        this._panel = panel;
        this._workspaceRoot = workspaceRoot;
        this._panel.webview.html = this._getHtml();
        this._sendState();
        this._sendAllEvents();
        // Watch state JSON files
        const stateWatcher = vscode.workspace.createFileSystemWatcher(new vscode.RelativePattern(workspaceRoot, '.claude/state/*.json'));
        stateWatcher.onDidChange(() => this._sendState(), null, this._disposables);
        stateWatcher.onDidCreate(() => this._sendState(), null, this._disposables);
        this._disposables.push(stateWatcher);
        // Watch events.jsonl for new lines
        const eventsWatcher = vscode.workspace.createFileSystemWatcher(new vscode.RelativePattern(workspaceRoot, '.claude/state/events.jsonl'));
        eventsWatcher.onDidChange(() => this._sendNewEvents(), null, this._disposables);
        eventsWatcher.onDidCreate(() => {
            this._eventLineCount = 0;
            this._sendAllEvents();
        }, null, this._disposables);
        this._disposables.push(eventsWatcher);
        // Handle messages from webview
        this._panel.webview.onDidReceiveMessage((msg) => {
            if (msg.command === 'refresh') {
                this._eventLineCount = 0;
                this._sendState();
                this._sendAllEvents();
            }
            else if (msg.command === 'invokeSkill' && msg.skill) {
                const inboxPath = path.join(this._workspaceRoot, '.claude', 'state', 'inbox.json');
                fs.writeFileSync(inboxPath, JSON.stringify({
                    skill: msg.skill, args: '',
                    requested_at: new Date().toISOString(),
                    status: 'pending'
                }, null, 2));
            }
            else if (msg.command === 'viewState') {
                const domain = readKernelDomain(this._workspaceRoot);
                const target = domain
                    ? path.join(this._workspaceRoot, '.claude', 'state', `${domain}_workflow.json`)
                    : path.join(this._workspaceRoot, '.claude', 'state', 'session_state.json');
                if (fs.existsSync(target)) {
                    vscode.window.showTextDocument(vscode.Uri.file(target));
                }
            }
        }, null, this._disposables);
        this._panel.onDidDispose(() => this.dispose(), null, this._disposables);
    }
    _sendState() {
        const stateDir = path.join(this._workspaceRoot, '.claude', 'state');
        const session = readJsonSafe(path.join(stateDir, 'session_state.json'));
        const domain = typeof session.domain === 'string' ? session.domain : undefined;
        const workflow = domain ? readJsonSafe(path.join(stateDir, `${domain}_workflow.json`)) : {};
        const inbox = readJsonSafe(path.join(stateDir, 'inbox.json'));
        const outbox = readJsonSafe(path.join(stateDir, 'outbox.json'));
        this._panel.webview.postMessage({
            command: 'state',
            domain: domain ?? 'none',
            anchored: workflow.anchored === true,
            actionsSince: typeof workflow.actions_since_anchor === 'number' ? workflow.actions_since_anchor : 0,
            actionsLimit: typeof workflow.actions_limit === 'number' ? workflow.actions_limit : 10,
            needsLearn: session.needs_learn === true,
            currentTask: typeof workflow.current_task === 'string' ? workflow.current_task : null,
            cycling: workflow.cycling === true,
            inboxStatus: typeof inbox.status === 'string' ? inbox.status : null,
            inboxSkill: typeof inbox.skill === 'string' ? inbox.skill : null,
            outboxStatus: typeof outbox.status === 'string' ? outbox.status : null,
            outboxSkill: typeof outbox.skill === 'string' ? outbox.skill : null,
        });
    }
    _sendAllEvents() {
        const eventsPath = path.join(this._workspaceRoot, '.claude', 'state', 'events.jsonl');
        if (!fs.existsSync(eventsPath))
            return;
        const lines = fs.readFileSync(eventsPath, 'utf8').split('\n').filter(l => l.trim());
        this._eventLineCount = lines.length;
        const events = lines.map(l => { try {
            return JSON.parse(l);
        }
        catch {
            return null;
        } }).filter(Boolean);
        this._panel.webview.postMessage({ command: 'allEvents', events });
    }
    _sendNewEvents() {
        const eventsPath = path.join(this._workspaceRoot, '.claude', 'state', 'events.jsonl');
        if (!fs.existsSync(eventsPath))
            return;
        const lines = fs.readFileSync(eventsPath, 'utf8').split('\n').filter(l => l.trim());
        if (lines.length < this._eventLineCount) {
            // File rotated — reload all
            this._eventLineCount = 0;
            this._sendAllEvents();
            return;
        }
        const newLines = lines.slice(this._eventLineCount);
        this._eventLineCount = lines.length;
        const events = newLines.map(l => { try {
            return JSON.parse(l);
        }
        catch {
            return null;
        } }).filter(Boolean);
        if (events.length > 0) {
            this._panel.webview.postMessage({ command: 'appendEvents', events });
        }
    }
    _getHtml() {
        return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Mission Control</title>
<style>
  *, *::before, *::after { box-sizing: border-box; }
  body {
    font-family: var(--vscode-font-family);
    font-size: var(--vscode-font-size);
    color: var(--vscode-foreground);
    background: var(--vscode-editor-background);
    margin: 0; padding: 0;
    display: flex; flex-direction: column; height: 100vh; overflow: hidden;
  }
  #header {
    padding: 8px 12px;
    border-bottom: 1px solid var(--vscode-panel-border);
    display: flex; align-items: center; justify-content: space-between;
    flex-shrink: 0;
  }
  #header h1 {
    font-size: 12px; font-weight: 700; margin: 0;
    letter-spacing: 0.08em; text-transform: uppercase;
  }
  #header-controls { display: flex; gap: 6px; }
  button {
    background: var(--vscode-button-secondaryBackground);
    color: var(--vscode-button-secondaryForeground);
    border: none; padding: 3px 8px; cursor: pointer;
    border-radius: 2px; font-size: 13px;
  }
  button:hover { background: var(--vscode-button-secondaryHoverBackground); }
  button.active { background: var(--vscode-button-background); color: var(--vscode-button-foreground); }
  #status {
    padding: 6px 12px;
    border-bottom: 1px solid var(--vscode-panel-border);
    font-size: 12px; display: flex; gap: 14px; align-items: center;
    flex-shrink: 0;
    background: var(--vscode-sideBar-background);
  }
  .badge { padding: 1px 7px; border-radius: 10px; font-size: 11px; }
  .badge-green  { background: #1a4a1a; color: #4ec94e; }
  .badge-yellow { background: #4a3a00; color: #f5c518; }
  .badge-red    { background: #4a1a1a; color: #f44747; }
  .badge-gray   { background: var(--vscode-badge-background); color: var(--vscode-badge-foreground); }
  #skills {
    padding: 5px 12px 6px;
    border-bottom: 1px solid var(--vscode-panel-border);
    display: flex; align-items: center; gap: 6px; flex-wrap: wrap;
    flex-shrink: 0;
  }
  #skills-label {
    font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em;
    color: var(--vscode-descriptionForeground); flex-shrink: 0; margin-right: 2px;
  }
  .skill-btn { font-size: 11px; padding: 2px 8px; }
  .skill-btn.contextual { display: none; }
  .skill-btn.contextual.visible { display: inline; }
  .skill-btn:disabled { opacity: 0.4; cursor: not-allowed; }
  #skill-status { font-size: 11px; color: var(--vscode-descriptionForeground); }
  #events-label {
    padding: 5px 12px 3px;
    font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em;
    color: var(--vscode-descriptionForeground);
    flex-shrink: 0;
  }
  #events {
    flex: 1; overflow-y: auto;
    font-family: var(--vscode-editor-font-family, monospace);
    font-size: 12px;
  }
  #empty { padding: 10px 12px; color: var(--vscode-descriptionForeground); font-style: italic; }
  .row {
    padding: 2px 12px; display: flex; gap: 8px; align-items: baseline;
    border-left: 2px solid transparent;
  }
  .row:hover { background: var(--vscode-list-hoverBackground); }
  .row.action        { border-left-color: #444; color: var(--vscode-foreground); }
  .row.test_pass     { border-left-color: #2a6a2a; color: #4ec94e; }
  .row.test_fail     { border-left-color: #6a2a2a; color: #f44747; }
  .row.blocked       { border-left-color: #6a2a2a; color: #f44747; }
  .row.anchor        { border-left-color: #1a4a6a; color: #569cd6; }
  .row.learn         { border-left-color: #1a4a6a; color: #569cd6; }
  .row.session_start { border-left-color: #555; color: #888; font-style: italic; }
  .ts     { color: var(--vscode-descriptionForeground); width: 68px; flex-shrink: 0; font-size: 11px; }
  .icon   { width: 14px; flex-shrink: 0; }
  .kind   { width: 72px; flex-shrink: 0; font-weight: 500; }
  .detail { flex: 1; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; color: var(--vscode-descriptionForeground); }
  .row.test_pass .detail, .row.test_fail .detail,
  .row.blocked .detail,   .row.anchor .detail, .row.learn .detail { color: inherit; }
</style>
</head>
<body>
<div id="header">
  <h1>Mission Control</h1>
  <div id="header-controls">
    <button id="btn-pause" title="Pause auto-scroll">⏸</button>
    <button id="btn-refresh" title="Refresh from disk">↺</button>
  </div>
</div>
<div id="status">
  <span id="st-anchor" class="badge badge-gray">—</span>
  <span id="st-actions">—</span>
  <span id="st-domain" style="color:var(--vscode-descriptionForeground)">—</span>
  <span id="st-task"   style="color:var(--vscode-descriptionForeground)"></span>
</div>
<div id="skills">
  <span id="skills-label">Skills</span>
  <button class="skill-btn contextual" id="sk-anchor" data-skill="/kernel/anchor" title="/kernel/anchor">⚓ Anchor</button>
  <button class="skill-btn contextual" id="sk-learn"  data-skill="/kernel/learn"  title="/kernel/learn">★ Learn</button>
  <button class="skill-btn"            id="sk-qa"     data-skill="/qa-workflow"    title="/qa-workflow">⚙ QA</button>
  <button class="skill-btn"            id="sk-tests"  data-skill="/run-test"       title="/run-test">▶ Tests</button>
  <button class="skill-btn"            id="sk-state"  data-skill="__view_state"    title="Open state file">👁 State</button>
  <span id="skill-status"></span>
</div>
<div id="events-label">Live Events</div>
<div id="events"><div id="empty">No events yet.</div></div>
<script>
  const vscode = acquireVsCodeApi();
  let paused = false;

  document.getElementById('btn-pause').addEventListener('click', () => {
    paused = !paused;
    const btn = document.getElementById('btn-pause');
    btn.classList.toggle('active', paused);
    btn.title = paused ? 'Resume auto-scroll' : 'Pause auto-scroll';
  });

  document.getElementById('btn-refresh').addEventListener('click', () => {
    vscode.postMessage({ command: 'refresh' });
  });

  // Skill palette
  let _lastOutboxSkill = null;
  document.querySelectorAll('.skill-btn[data-skill]').forEach(btn => {
    btn.addEventListener('click', () => {
      const skill = btn.getAttribute('data-skill');
      if (skill === '__view_state') {
        vscode.postMessage({ command: 'viewState' });
      } else {
        vscode.postMessage({ command: 'invokeSkill', skill });
      }
    });
  });

  function updateSkills(msg) {
    // Contextual visibility
    document.getElementById('sk-anchor').classList.toggle('visible', !msg.anchored && !msg.needsLearn);
    document.getElementById('sk-learn').classList.toggle('visible',  msg.needsLearn === true);
    // Disable all when busy
    const busy = msg.inboxStatus === 'pending' || msg.inboxStatus === 'processing';
    document.querySelectorAll('.skill-btn').forEach(b => { b.disabled = busy; });
    // Status indicator
    const statusEl = document.getElementById('skill-status');
    if (busy) {
      statusEl.textContent = 'Running ' + (msg.inboxSkill || '…');
    } else if (msg.outboxStatus === 'done' && msg.outboxSkill && msg.outboxSkill !== _lastOutboxSkill) {
      _lastOutboxSkill = msg.outboxSkill;
      statusEl.textContent = '✓ ' + msg.outboxSkill;
      setTimeout(() => { if (statusEl.textContent.startsWith('✓')) statusEl.textContent = ''; }, 3000);
    } else if (!busy) {
      // Clear if not already showing a recent completion
      if (!statusEl.textContent.startsWith('✓')) statusEl.textContent = '';
    }
  }

  function updateStatus(msg) {
    const anchorEl  = document.getElementById('st-anchor');
    const actionsEl = document.getElementById('st-actions');
    const domainEl  = document.getElementById('st-domain');
    const taskEl    = document.getElementById('st-task');

    domainEl.textContent = 'Domain: ' + msg.domain;

    if (msg.needsLearn) {
      anchorEl.textContent = '✗ learn needed';
      anchorEl.className = 'badge badge-red';
    } else if (!msg.anchored) {
      anchorEl.textContent = '✗ anchor needed';
      anchorEl.className = 'badge badge-red';
    } else {
      anchorEl.textContent = '⚓ Anchored';
      anchorEl.className = 'badge badge-green';
    }

    const pct = msg.actionsLimit > 0 ? msg.actionsSince / msg.actionsLimit : 0;
    actionsEl.textContent = msg.actionsSince + '/' + msg.actionsLimit + ' actions';
    actionsEl.style.color = pct >= 0.8 ? '#f5c518' : '';

    taskEl.textContent = (msg.cycling && msg.currentTask) ? 'Task: ' + msg.currentTask : '';
  }

  function icon(type) {
    switch (type) {
      case 'test_pass': return '✓';
      case 'test_fail': return '✗';
      case 'blocked':   return '✗';
      case 'anchor':    return '⚓';
      case 'learn':     return '★';
      default:          return '·';
    }
  }

  function kindLabel(type, tool) {
    return type === 'action' ? (tool || 'action') : type;
  }

  function shortDetail(detail) {
    if (!detail) return '';
    const parts = detail.split('/');
    return parts.length > 2 ? parts.slice(-2).join('/') : detail;
  }

  function fmtTs(ts) {
    try {
      return new Date(ts).toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' });
    } catch { return ts || ''; }
  }

  function makeRow(ev) {
    const row = document.createElement('div');
    row.className = 'row ' + (ev.type || 'action');
    const detailFull  = ev.detail || '';
    const detailShort = shortDetail(detailFull);
    row.innerHTML =
      '<span class="ts">'     + fmtTs(ev.ts)                                         + '</span>' +
      '<span class="icon">'   + icon(ev.type)                                         + '</span>' +
      '<span class="kind">'   + kindLabel(ev.type, ev.tool)                           + '</span>' +
      '<span class="detail" title="' + detailFull.replace(/"/g, '&quot;') + '">' + detailShort + '</span>';
    return row;
  }

  function appendEvents(events) {
    const container = document.getElementById('events');
    const empty = document.getElementById('empty');
    if (empty) empty.remove();
    for (const ev of events) container.appendChild(makeRow(ev));
    if (!paused) container.scrollTop = container.scrollHeight;
  }

  function setAllEvents(events) {
    const container = document.getElementById('events');
    container.innerHTML = events.length === 0 ? '<div id="empty">No events yet.</div>' : '';
    for (const ev of events) container.appendChild(makeRow(ev));
    if (!paused) container.scrollTop = container.scrollHeight;
  }

  window.addEventListener('message', ev => {
    const msg = ev.data;
    if      (msg.command === 'state')        { updateStatus(msg); updateSkills(msg); }
    else if (msg.command === 'allEvents')    setAllEvents(msg.events);
    else if (msg.command === 'appendEvents') appendEvents(msg.events);
  });
</script>
</body>
</html>`;
    }
    dispose() {
        MissionControlPanel.currentPanel = undefined;
        this._panel.dispose();
        while (this._disposables.length) {
            const d = this._disposables.pop();
            if (d)
                d.dispose();
        }
    }
}
// ---------------------------------------------------------------------------
// Discovery
// ---------------------------------------------------------------------------
function relId(absPath, root) {
    return path.relative(root, absPath);
}
async function discoverAll(ctrl, root) {
    const uris = await vscode.workspace.findFiles(new vscode.RelativePattern(root, 'tests/**/*.py'), '**/conftest.py');
    await Promise.all(uris.map(uri => updateFile(ctrl, uri)));
}
async function updateFile(ctrl, uri) {
    const basename = path.basename(uri.fsPath);
    if (!basename.startsWith('test_') || basename === 'conftest.py')
        return;
    let src;
    try {
        src = fs.readFileSync(uri.fsPath, 'utf8');
    }
    catch {
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
    let currentClass = null;
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        const classMatch = line.match(RE_TEST_CLASS);
        if (classMatch) {
            const className = classMatch[1];
            const classId = `${fileId}::${className}`;
            const classItem = ctrl.createTestItem(classId, className, uri);
            classItem.range = new vscode.Range(i, 0, i, line.length);
            fileItem.children.add(classItem);
            currentClass = classItem;
            continue;
        }
        const methodMatch = line.match(RE_TEST_METHOD);
        if (methodMatch && currentClass) {
            const methodName = methodMatch[1];
            const methodId = `${currentClass.id}::${methodName}`;
            const methodItem = ctrl.createTestItem(methodId, methodName, uri);
            methodItem.range = new vscode.Range(i, 0, i, line.length);
            currentClass.children.add(methodItem);
        }
    }
}
// ---------------------------------------------------------------------------
// Running
// ---------------------------------------------------------------------------
async function runHandler(ctrl, request, token, root) {
    const run = ctrl.createTestRun(request);
    // Collect leaf test items and their pytest node IDs
    const leafItems = [];
    function collect(item) {
        if (request.exclude?.includes(item))
            return;
        if (item.children.size === 0) {
            leafItems.push(item);
        }
        else {
            item.children.forEach(collect);
        }
    }
    if (request.include) {
        request.include.forEach(collect);
    }
    else {
        ctrl.items.forEach(collect);
    }
    // Mark all as enqueued before starting
    leafItems.forEach(item => run.enqueued(item));
    // Build pytest args
    const config = vscode.workspace.getConfiguration('platformSelenium');
    const extraArgs = config.get('pytestArgs') ?? [];
    const nodeIds = leafItems.map(i => i.id);
    const args = [
        '-m', 'pytest',
        ...nodeIds,
        '-v',
        '--tb=short',
        '--no-header',
        '-p', 'no:cacheprovider',
        ...extraArgs,
    ];
    const python = resolvePython(root, config.get('pythonPath'));
    run.appendOutput(`\x1b[36m$ ${python} ${args.join(' ')}\x1b[0m\r\n\r\n`);
    // Mark leaves as started
    leafItems.forEach(item => run.started(item));
    // Spawn pytest
    const proc = (0, child_process_1.spawn)(python, args, { cwd: root, env: process.env });
    token.onCancellationRequested(() => proc.kill());
    let stdout = '';
    proc.stdout?.on('data', (chunk) => {
        const text = chunk.toString();
        stdout += text;
        run.appendOutput(text.replace(/\n/g, '\r\n'));
    });
    proc.stderr?.on('data', (chunk) => {
        run.appendOutput(chunk.toString().replace(/\n/g, '\r\n'));
    });
    await new Promise(resolve => proc.on('close', resolve));
    // Build a map of testId → failure message from the short-summary section
    const failMessages = parseFailureSummary(stdout);
    // Map results back to TestItems
    const itemById = new Map(leafItems.map(i => [i.id, i]));
    for (const line of stdout.split('\n')) {
        const m = line.match(RE_RESULT);
        if (!m)
            continue;
        const [, testId, status] = m;
        const item = itemById.get(testId);
        if (!item)
            continue;
        if (status === 'PASSED') {
            run.passed(item);
        }
        else {
            const detail = failMessages.get(testId) ?? 'Test failed';
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
function parseFailureSummary(output) {
    const map = new Map();
    let inSummary = false;
    for (const line of output.split('\n')) {
        if (line.includes('short test summary info')) {
            inSummary = true;
            continue;
        }
        if (!inSummary)
            continue;
        if (line.startsWith('='))
            break; // end of summary section
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
function resolvePython(root, configured) {
    if (configured && configured.trim())
        return configured.trim();
    const candidates = [
        path.join(root, 'venv', 'bin', 'python'),
        path.join(root, 'venv', 'Scripts', 'python.exe'),
        path.join(root, '.venv', 'bin', 'python'),
        path.join(root, '.venv', 'Scripts', 'python.exe'),
    ];
    for (const p of candidates) {
        if (fs.existsSync(p))
            return p;
    }
    return 'python3';
}
//# sourceMappingURL=extension.js.map