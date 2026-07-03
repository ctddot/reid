"""Nyx: redteam/offensive-security assistant persona.

Swaps only the agent's system prompt — tool access and policy gating are
unchanged, since the ToolRegistry/PolicyEngine (not the prompt) is the real
safety boundary. Same philosophy as DeepReid's role prompts: the restriction
that matters is what tools are registered and how the policy engine gates
them, not what the model is told to refuse.
"""
from __future__ import annotations

from reidcli.personas.store import BUILTIN_PERSONAS

NYX_SYSTEM_PROMPT = BUILTIN_PERSONAS["nyx"].system_prompt

__all__ = ["NYX_SYSTEM_PROMPT"]
