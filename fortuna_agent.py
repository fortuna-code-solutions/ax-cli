#!/usr/bin/env python3
"""fortuna-bot — a demo agent for the aX platform.

Run via: ax listen --agent fortuna-bot --exec "python fortuna_agent.py"

Commands:
  @fortuna-bot help        — list available commands
  @fortuna-bot status      — workspace summary
  @fortuna-bot tasks       — list open tasks
  @fortuna-bot agents      — list agents in the space
  @fortuna-bot echo <text> — echo back the text
  @fortuna-bot flip        — flip a coin
  @fortuna-bot roll        — roll a d20
"""
from __future__ import annotations
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def _get_client():
    from ax_cli.config import get_client
    return get_client()


def get_command(text: str) -> tuple[str, str]:
    clean = text.strip()
    for prefix in ["@fortuna-bot", "@fortuna_bot", "fortuna-bot", "fortuna_bot"]:
        if clean.lower().startswith(prefix):
            clean = clean[len(prefix):].strip()
            break
    parts = clean.split(None, 1)
    cmd = parts[0].lower() if parts else ""
    arg = parts[1] if len(parts) > 1 else ""
    return cmd, arg


def cmd_help() -> str:
    return """Available commands:
- **help** — this message
- **status** — workspace summary
- **tasks** — list open tasks
- **agents** — list agents in the space
- **echo <text>** — echo back your text
- **flip** — flip a coin
- **roll** — roll a d20
- or just say anything and I'll respond"""


def cmd_status() -> str:
    try:
        c = _get_client()
        spaces = c.list_spaces()
        space_count = spaces.get("count", len(spaces.get("spaces", [])))
        agents = c.list_agents()
        agent_list = agents.get("agents", [])
        tasks = c.list_tasks(limit=50)
        task_list = tasks.get("tasks", tasks) if isinstance(tasks, dict) else tasks
        if isinstance(task_list, list):
            open_tasks = [t for t in task_list if t.get("status") not in ("completed", "cancelled")]
        else:
            open_tasks = []
        return (
            f"**Workspace Status**\n"
            f"- Spaces: {space_count}\n"
            f"- Agents: {len(agent_list)} ({', '.join(a['name'] for a in agent_list[:5])})\n"
            f"- Open tasks: {len(open_tasks)}"
        )
    except Exception as e:
        return f"Could not fetch status: {e}"


def cmd_tasks() -> str:
    try:
        c = _get_client()
        tasks = c.list_tasks(limit=10)
        task_list = tasks.get("tasks", tasks) if isinstance(tasks, dict) else tasks
        if not task_list or (isinstance(task_list, list) and len(task_list) == 0):
            return "No tasks found. Create one with `ax tasks create \"title\"`"
        lines = ["**Tasks:**"]
        for t in (task_list if isinstance(task_list, list) else []):
            status = t.get("status", "unknown")
            title = t.get("title", "untitled")
            lines.append(f"- [{status}] {title}")
        return "\n".join(lines)
    except Exception as e:
        return f"Could not fetch tasks: {e}"


def cmd_agents() -> str:
    try:
        c = _get_client()
        agents = c.list_agents()
        agent_list = agents.get("agents", [])
        if not agent_list:
            return "No agents in this space."
        lines = ["**Agents in this space:**"]
        for a in agent_list:
            name = a.get("name", "unknown")
            desc = a.get("description", "")
            lines.append(f"- **{name}** — {desc}" if desc else f"- **{name}**")
        return "\n".join(lines)
    except Exception as e:
        return f"Could not fetch agents: {e}"


def cmd_flip() -> str:
    return random.choice(["Heads!", "Tails!"])


def cmd_roll() -> str:
    result = random.randint(1, 20)
    if result == 20:
        return "**NAT 20!** Critical success!"
    elif result == 1:
        return "**NAT 1.** Critical fail."
    return f"You rolled a **{result}**."


def main():
    mention_content = os.environ.get("AX_MENTION_CONTENT", "")
    if not mention_content and len(sys.argv) > 1:
        mention_content = sys.argv[1]

    cmd, arg = get_command(mention_content)

    handlers = {
        "help": cmd_help,
        "status": cmd_status,
        "tasks": cmd_tasks,
        "agents": cmd_agents,
        "echo": lambda: arg if arg else "Echo what? Usage: `@fortuna-bot echo <text>`",
        "flip": cmd_flip,
        "roll": cmd_roll,
    }

    if cmd in handlers:
        print(handlers[cmd]())
    elif not cmd:
        print("Hey! I'm fortuna-bot. Say `@fortuna-bot help` to see what I can do.")
    else:
        print(f"I don't know `{cmd}` yet. Try `@fortuna-bot help` for available commands.")


if __name__ == "__main__":
    main()
