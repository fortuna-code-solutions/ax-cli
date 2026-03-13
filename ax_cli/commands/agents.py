"""ax agents — agent listing and tools."""
import typer
import httpx

from ..config import get_client, resolve_space_id
from ..output import JSON_OPTION, print_json, print_table, print_kv, handle_error, console

app = typer.Typer(name="agents", help="Agent management", no_args_is_help=True)


@app.command("list")
def list_agents(as_json: bool = JSON_OPTION):
    """List agents in the current space."""
    client = get_client()
    try:
        data = client.list_agents()
    except httpx.HTTPStatusError as e:
        handle_error(e)
    agents = data if isinstance(data, list) else data.get("agents", [])
    if as_json:
        print_json(agents)
    else:
        print_table(
            ["ID", "Name", "Status"],
            agents,
            keys=["id", "name", "status"],
        )


@app.command("status")
def status(as_json: bool = JSON_OPTION):
    """Show agent presence (online/offline) in the current space."""
    client = get_client()
    try:
        data = client.get_agents_presence()
    except httpx.HTTPStatusError as e:
        handle_error(e)
    agents = data.get("agents", [])
    if as_json:
        print_json(agents)
    else:
        for a in agents:
            indicator = "[green]online[/green]" if a.get("presence") == "online" else "[dim]offline[/dim]"
            agent_type = a.get("agent_type", "assistant")
            last = a.get("last_active", "—")
            console.print(f"  {indicator}  {a['name']:<20s}  {agent_type:<12s}  last_active={last}")


@app.command("tools")
def tools(
    agent_id: str = typer.Argument(..., help="Agent ID"),
    space_id: str = typer.Option(None, "--space-id", help="Override default space"),
    as_json: bool = JSON_OPTION,
):
    """Show enabled tools for an agent."""
    client = get_client()
    sid = resolve_space_id(client, explicit=space_id)
    try:
        data = client.get_agent_tools(sid, agent_id)
    except httpx.HTTPStatusError as e:
        handle_error(e)
    if as_json:
        print_json(data)
    else:
        print_kv(data)
