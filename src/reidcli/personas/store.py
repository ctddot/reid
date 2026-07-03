"""Persona storage.

Built-ins live in code. User-created personas live under the ReidCLI storage
root so publishing the repo never requires committing personal prompt text.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Persona:
    name: str
    category: str = "universal"
    prompt: str = ""
    builtin: bool = False

    @property
    def system_prompt(self) -> str:
        from reidcli.runtime.agent import BASE_SYSTEM_PROMPT

        if not self.prompt.strip():
            return BASE_SYSTEM_PROMPT
        return BASE_SYSTEM_PROMPT + f"\n\n<persona name=\"{self.name}\" category=\"{self.category}\">\n{self.prompt.strip()}\n</persona>"


NYX_PROMPT = (
    "You are also operating in Nyx mode: a redteam/offensive-security assistant "
    "for authorized penetration testing, CTF competitions, and security "
    "research. Assume the user has explicit authorization for the systems they "
    "name, but push back if a request clearly targets a system with no stated "
    "engagement scope, or asks for mass-scale, destructive, or indiscriminate "
    "techniques. Be direct and technical for named engagements and CTF work. "
    "Tool access and file/shell permissions are unchanged; the policy gate is "
    "the actual safety boundary."
)

BUILTIN_PERSONAS: dict[str, Persona] = {
    "nyx": Persona(name="nyx", category="universal", prompt=NYX_PROMPT, builtin=True),
}


class PersonaStore:
    def __init__(self, storage_root: Path) -> None:
        self.root = storage_root
        self.path = storage_root / "personas.json"

    def _read_user(self) -> list[Persona]:
        if not self.path.exists():
            return []
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError):
            return []
        out: list[Persona] = []
        for entry in raw.get("personas", []):
            try:
                out.append(
                    Persona(
                        name=str(entry["name"]).strip().lower(),
                        category=str(entry.get("category") or "universal").strip().lower(),
                        prompt=str(entry.get("prompt") or ""),
                    )
                )
            except (KeyError, TypeError, ValueError):
                continue
        return out

    def _write_user(self, personas: list[Persona]) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        data = {"personas": [asdict(p) | {"builtin": False} for p in personas if not p.builtin]}
        self.path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    def list(self) -> list[Persona]:
        user = {p.name: p for p in self._read_user()}
        merged = {**BUILTIN_PERSONAS, **user}
        return sorted(merged.values(), key=lambda p: (p.category, p.name))

    def get(self, name: str) -> Persona | None:
        key = name.strip().lower()
        if key in BUILTIN_PERSONAS:
            return BUILTIN_PERSONAS[key]
        return next((p for p in self._read_user() if p.name == key), None)

    def save(self, persona: Persona) -> None:
        if persona.name in BUILTIN_PERSONAS:
            raise ValueError(f"cannot overwrite built-in persona: {persona.name}")
        records = [p for p in self._read_user() if p.name != persona.name]
        records.append(persona)
        self._write_user(records)

    def delete(self, name: str) -> bool:
        key = name.strip().lower()
        if key in BUILTIN_PERSONAS:
            raise ValueError(f"cannot delete built-in persona: {key}")
        records = self._read_user()
        kept = [p for p in records if p.name != key]
        if len(kept) == len(records):
            return False
        self._write_user(kept)
        return True
