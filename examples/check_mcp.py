#!/usr/bin/env python3
"""Talk to the Sports Betting Odds MCP server the way an MCP client does: initialize, list the tools, call one.

    export RAPIDAPI_KEY=your-key          # free BASIC plan on RapidAPI
    python examples/check_mcp.py          # Python 3.9+, standard library only

The server is stateless MCP over Streamable HTTP: every message is one POST with a JSON-RPC 2.0 body, and every
answer is plain JSON (no SSE stream, no session id).
"""
import json
import os
import urllib.request

HOST = "sports-betting-odds-arbitrage-api.p.rapidapi.com"
URL = f"https://{HOST}/v1/mcp"


def rpc(method, params=None, msg_id=1, url=URL, headers=None):
    """Send one JSON-RPC message; return the parsed answer (None for a notification, which gets 202)."""
    body = {"jsonrpc": "2.0", "method": method}
    if msg_id is not None:
        body["id"] = msg_id
    if params is not None:
        body["params"] = params
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                                 headers={"Content-Type": "application/json",
                                          "Accept": "application/json, text/event-stream", **(headers or {})})
    with urllib.request.urlopen(req, timeout=60) as r:
        raw = r.read()
    return json.loads(raw) if raw else None


def main(url=URL, headers=None):
    init = rpc("initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                              "clientInfo": {"name": "check_mcp", "version": "1.0"}}, url=url, headers=headers)
    server = init["result"]["serverInfo"]
    print(f"connected: {server['title']} {server['version']}, protocol {init['result']['protocolVersion']}")
    rpc("notifications/initialized", msg_id=None, url=url, headers=headers)

    tools = rpc("tools/list", msg_id=2, url=url, headers=headers)["result"]["tools"]
    print(f"{len(tools)} tools:", ", ".join(t["name"] for t in tools))

    res = rpc("tools/call", {"name": "list_leagues", "arguments": {}}, msg_id=3, url=url, headers=headers)["result"]
    if res.get("isError"):
        raise SystemExit(res["content"][0]["text"])
    data = res["structuredContent"]
    print(f"plan {data.get('plan')}: {len(data['leagues'])} leagues, e.g.",
          ", ".join(f"{x['key']} ({x['sport']})" for x in data["leagues"][:5]))


if __name__ == "__main__":
    key = os.environ.get("RAPIDAPI_KEY")
    if not key:
        raise SystemExit("Set RAPIDAPI_KEY first (subscribe to the API on RapidAPI; BASIC is free).")
    main(headers={"X-RapidAPI-Key": key, "X-RapidAPI-Host": HOST})
