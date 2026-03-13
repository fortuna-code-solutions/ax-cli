"""aX Platform CLI — Typer app with subcommand registration."""
from typing import Optional

import typer

from .commands import auth, keys, agents, messages, tasks, events

app = typer.Typer(name="ax", help="aX Platform CLI", no_args_is_help=True)
app.add_typer(auth.app, name="auth")
app.add_typer(keys.app, name="keys")
app.add_typer(agents.app, name="agents")
app.add_typer(messages.app, name="messages")
app.add_typer(tasks.app, name="tasks")
app.add_typer(events.app, name="events")


@app.command("send")
def send_shortcut(
    content: str = typer.Argument(..., help="Message to send"),
    wait: bool = typer.Option(True, "--wait/--no-wait", "-w", help="Wait for aX response (default: yes)"),
    timeout: int = typer.Option(60, "--timeout", "-t", help="Max seconds to wait"),
    agent: Optional[str] = typer.Option(None, "--agent", "-a", help="Send as agent (X-Agent-Name)"),
    space_id: Optional[str] = typer.Option(None, "--space-id", "-s", help="Override default space"),
    as_json: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """Send a message and wait for aX's response. Shortcut for: ax messages send --wait"""
    messages.send(
        content=content,
        wait=wait,
        timeout=timeout,
        agent_id=None,
        agent_name=agent,
        channel="main",
        parent=None,
        space_id=space_id,
        as_json=as_json,
    )
