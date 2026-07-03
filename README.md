# ReidCLI

Terminal-native personal intelligence and coding CLI with an agent-first runtime.

ReidCLI is not just a chat wrapper. It has sessions, tasks, provider adapters,
tool calls, policy gates, slash commands, workflows, subagents, DeepReid
planning, Nyx mode, and structured persistence.

## Latest Update

Version `0.1.3` focuses on making ReidCLI feel like a clean native terminal AI
CLI:

- Native terminal scrollback instead of a broken full-screen scroll mode.
- Red outlined input box that resizes with the terminal.
- Claude Code-style slash command menu with ReidCLI red coloring.
- Arrow-key navigation inside the slash command menu.
- `/models` shows GPT, Claude/Sonnet, Gemini, Groq, Kimi, Ollama, and connected provider defaults.
- `/persona` adds, lists, shows, uses, and deletes custom personas.
- ReidVerse provider support as the intended default provider.
- Better thinking/status behavior under the input box.
- Friendlier provider errors instead of noisy stack traces.
- Experimental `tui-test` command kept separate for UI work.
- npm/npx packaging support.

## Quick Start

### Run From Source

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
reidcli
```

On macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
reidcli
```

### Run With uv

```powershell
uv run reidcli
```

### Run With npx

After the npm package is published:

```powershell
npx reidcli
```

## Commands

Top-level commands:

| Command | Purpose |
|---|---|
| `reidcli` | Launch interactive mode |
| `reidcli interactive` | Launch interactive mode explicitly |
| `reidcli tui-test` | Launch the experimental UI test command |
| `reidcli exec "<prompt>"` | Run one prompt headlessly |
| `reidcli deepreid "<task>"` | Plan and review a task with Researcher/Planner/Critic agents |
| `reidcli resume <session-id>` | Resume a previous session |
| `reidcli sessions` | List saved sessions |
| `reidcli config-show` | Show merged configuration |
| `reidcli tools` | List tools |
| `reidcli doctor` | Run diagnostics |
| `reidcli version` | Show version/runtime info |

Inside interactive mode, type `/` to open the slash command menu. The menu is
keyboard navigable with arrow keys and Enter.

Important slash commands:

| Command | Purpose |
|---|---|
| `/status` | Show current session, mode, provider, model, and tasks |
| `/usage` | Show transcript/token usage |
| `/providers` | List registered providers |
| `/connect` | Add a provider |
| `/disconnect` | Remove a saved provider |
| `/use <name>` | Switch active provider |
| `/models` | Show local model catalog and connected provider defaults |
| `/model <name>` | Set model for the session |
| `/persona list` | List built-in and custom personas |
| `/persona add <name> <category> <prompt>` | Save a persona under `universal` or a model/provider category |
| `/persona use <name>` | Switch to a persona |
| `/persona use off` | Return to the default persona |
| `/persona show <name>` | Show persona prompt text |
| `/persona delete <name>` | Delete a custom persona |
| `/sessions` | List sessions |
| `/session rename ...` | Rename a session |
| `/session delete ...` | Delete a session |
| `/search <text>` | Search saved transcripts |
| `/transcript [n]` | Show recent transcript messages |
| `/undo` | Remove last assistant/tool output but keep prompt |
| `/retry` | Rerun last user prompt |
| `/edit` | Edit last user prompt and rerun |
| `/fork` | Fork the current session |
| `/compact` | Compact conversation context |
| `/plan` | Toggle planning mode |
| `/tools enable ...` | Enable a tool |
| `/tools disable ...` | Disable a tool |
| `/approvals` | Show approval policy |
| `/cost` | Show cost/usage information |
| `/web` | Toggle web behavior |
| `/prompt save ...` | Save a reusable prompt |
| `/prompt run ...` | Run a saved prompt |
| `/workflows save ...` | Save a workflow |
| `/workflows run ...` | Run a workflow |
| `/workflows show ...` | Show workflow steps |
| `/workflows delete ...` | Delete a workflow |
| `/mcp list` | List MCP connections |
| `/mcp connect ...` | Connect MCP |
| `/mcp disconnect ...` | Disconnect MCP |
| `/agents` | Show agent/subagent info |
| `/deepreid` | Run DeepReid planning |
| `/theme` | Change theme |
| `/keys` | Show key bindings |
| `/update` | Show update information |
| `/clear` | Clear screen |
| `/exit` | Exit ReidCLI |

## Interactive UI

The default interface uses normal terminal scrollback. This means output stays
in your terminal history and resizes naturally when the window gets wider or
narrower.

Current UI behavior:

- Red outlined prompt box.
- Native terminal scroll.
- Slash command menu that scales to the terminal width.
- Arrow-key navigation in the command menu.
- `Shift+Tab` cycles interaction modes:
  - `plan` uses a blue input box and hides edit/write/shell tools.
  - `accept edits` uses the red input box and accepts file edits.
  - `automation` uses a green input box and enables autonomous workflow state.
- Compact thinking line under the active prompt.
- `Ctrl+B` toggles live activity details while a turn is running, such as
  reading files, searching directories, editing files, running commands, or
  waiting for the model.
- `Esc` once asks for stop confirmation.
- `Esc` again interrupts the running turn.

The older full-screen implementation still exists internally as fallback code,
but the active default path is the native terminal UI.

## Providers

`stub` is available as an offline deterministic provider.

ReidCLI also supports:

- Anthropic
- OpenAI
- OpenAI-compatible APIs
- Ollama
- Gemini
- Groq through OpenAI-compatible endpoints
- Kimi through OpenAI-compatible endpoints
- ReidVerse through OpenAI-compatible configuration

Provider records are stored in:

```text
~/.reidcli/providers.json
```

Global config is stored in:

```text
~/.reidcli/config.json
```

PowerShell-written provider files with UTF-8 BOM are supported.

## Configuration

Configuration is merged from:

1. Built-in defaults
2. Global config
3. Project config
4. `settings.json`
5. Environment variables

Useful environment variables:

| Variable | Purpose |
|---|---|
| `REIDCLI_PROVIDER` | Default provider name |
| `REIDCLI_WORKSPACE` | Workspace path |
| `REIDCLI_STORAGE` | Storage path |
| `REIDCLI_PERMISSION_MODE` | `strict`, `balanced`, `autonomous`, or `custom` |
| `ANTHROPIC_API_KEY` | Anthropic key |
| `OPENAI_API_KEY` | OpenAI/OpenAI-compatible key |
| `GEMINI_API_KEY` | Gemini key |

Do not commit real provider keys.

## Tools

Tools are policy-gated.

| Tool | Purpose |
|---|---|
| `read_file` | Read file content |
| `write_file` | Write file content |
| `patch_file` | Apply exact text replacement |
| `list_dir` | List directory entries |
| `find_files` | Find files by glob |
| `grep_files` | Search file contents |
| `run_command` | Run shell command |
| `web_search` | Search the web |
| `spawn_agent` | Run a scoped child agent |

## DeepReid

DeepReid is a Researcher -> Planner -> Critic pipeline for planning and
reviewing work before implementation.

```powershell
reidcli deepreid "plan this task"
```

DeepReid writes Markdown results to:

```text
~/.reidcli/deepreid/
```

## Nyx Mode

Nyx is a redteam/offensive-security persona for authorized work.

```powershell
reidcli --nyx
reidcli exec --nyx "authorized security task"
```

Inside interactive mode:

```text
/nyx on
/nyx off
```

Nyx changes the assistant persona only. Tool access is still controlled by the
same policy engine.

## Personas

Personas are reusable system-prompt add-ons. ReidCLI includes `nyx` as a
built-in universal persona and lets users create their own.

```text
/persona list
/persona add writer universal keep answers concise and polished
/persona add gemini-helper gemini explain Gemini-specific tradeoffs clearly
/persona use writer
/persona use off
```

Categories can be broad, like `universal`, or tied to a model/provider family,
like `gemini`, `groq`, `kimi`, `sonnet`, or `ollama`.

Custom personas are stored in:

```text
~/.reidcli/personas.json
```

## Development

Run checks:

```powershell
$env:PYTHONPATH='src'
uv run ruff check src tests
uv run pytest
npm pack --dry-run
```

Current verified test status:

```text
52 passed
```

## Project Structure

```text
ReidCLI/
  bin/                 npm executable wrapper
  scripts/             install helpers
  src/reidcli/
    app/               Typer app and dependency wiring
    automation/        headless execution support
    config/            config models and loader
    deepreid/          Researcher/Planner/Critic pipeline
    diagnostics/       logging and diagnostics
    integrations/      MCP foundation
    nyx/               Nyx persona
    personas/          built-in persona catalog and user persona store
    policy/            permission modes and policy engine
    provider/          provider adapters and registry
    runtime/           agent loop, orchestrator, subagents
    session/           sessions and transcript storage
    tasks/             task state
    tools/             tool registry and implementations
    ui/                terminal UI, rendering, slash commands
    workflows/         reusable workflow storage
  tests/               test suite
```

## License

MIT
