"""Interactive REPL entry point.

Thin wrapper around the terminal chat UI in ui.app, kept as a separate module
so app/commands.py's `from reidcli.ui.repl import repl` stays stable.
"""
from __future__ import annotations

from reidcli.runtime.orchestrator import Orchestrator
from reidcli.ui import app


def repl(orchestrator: Orchestrator, initial_prompt: str | None = None) -> int:
    return app.run(orchestrator, initial_prompt=initial_prompt)
