# Sports Betting Odds MCP Server

[![Sports Betting Odds & Arbitrage MCP connector](https://glama.ai/mcp/connectors/dev.minmaxxxer/sports-betting-odds/badges/score.svg)](https://glama.ai/mcp/connectors/dev.minmaxxxer/sports-betting-odds)

An MCP server with sports betting odds data for Claude, Cursor, VS Code and any other MCP client:
- closing lines of **390,000+ past games** with every bet already graded;
- **Pinnacle's current lines**, in-play included, and **player props**;
- **arbitrage** and **value bets** on the coming games.

It is a remote server (Streamable HTTP, stateless JSON). Data is sold through RapidAPI, so all you need is a RapidAPI key. The BASIC plan is free.

```
https://api.minmaxxxer.dev/mcp
header: X-RapidAPI-Key: <your key>
```

Listing the tools needs no key and costs nothing. Each tool call goes to RapidAPI with your key and counts as one request of your plan. The same server also answers directly on RapidAPI:

```
https://sports-betting-odds-arbitrage-api.p.rapidapi.com/v1/mcp
headers: X-RapidAPI-Key: <your key>
         X-RapidAPI-Host: sports-betting-odds-arbitrage-api.p.rapidapi.com
```

## What an agent can answer

| Ask | Tool |
|---|---|
| "How did NBA home favourites do against the spread in 2024-25?" | `get_closing_lines` |
| "What is Pinnacle's line on tonight's Celtics game?" | `get_pinnacle_odds` |
| "Any surebets on this weekend's Premier League games?" | `find_arbitrage` |
| "Which NBA player props moved most since they opened?" | `get_player_props` |
| "Did the closing line beat the opening one for the Chiefs this season?" | `get_closing_lines`, `get_line_movement` |

## Tools

Each tool runs the REST endpoint of the same name. Answers, plan limits and error messages are the same as REST, and one tool call is one API request.

| Tool | Returns |
|---|---|
| `list_leagues` | League keys, seasons and the first season your plan covers. Call this first. |
| `get_closing_lines` | One row per finished game: opening and closing odds, implied probabilities, graded bets. |
| `get_games` | Games by season, day or date range, with scores, every bookmaker's odds and match stats. |
| `get_scores` | Compact scores and statuses for one league-local day. |
| `get_upcoming_odds` | Coming games with every bookmaker's current prices. |
| `get_best_odds` | The best price of every outcome and the bookmaker offering it. |
| `get_line_movement` | Coming games whose market moved most since the opening. |
| `find_arbitrage` | Surebets across bookmakers, with the stake split. |
| `find_value_bets` | Prices above the market's no-vig fair odds. |
| `get_pinnacle_odds` | Pinnacle's current moneyline, main spread and main total, re-read every 2 minutes before the start. |
| `get_pinnacle_closing_lines` | Pinnacle's opening and closing lines of a past day. |
| `get_player_props` | Pinnacle player props now: line, odds, no-vig probability, opening line. |
| `get_player_props_history` | Graded props of a past day: closing line, result, the player's actual stat. |
| `list_teams` | Teams of a league with their IDs. |
| `list_bookmakers` | The bookmakers behind a league's odds. |
| `get_game` | One game by ID with every bookmaker's odds. |

## Connect

**Claude Code**

```bash
claude mcp add --transport http sports-odds https://api.minmaxxxer.dev/mcp --header "X-RapidAPI-Key: YOUR_KEY"
```

**Cursor** (`~/.cursor/mcp.json`)

```json
{"mcpServers": {"sports-odds": {
  "url": "https://api.minmaxxxer.dev/mcp",
  "headers": {"X-RapidAPI-Key": "YOUR_KEY"}}}}
```

**VS Code** (`.vscode/mcp.json`)

```json
{"servers": {"sports-odds": {"type": "http",
  "url": "https://api.minmaxxxer.dev/mcp",
  "headers": {"X-RapidAPI-Key": "YOUR_KEY"}}}}
```

**Claude Desktop** and other clients without custom headers, through the [`mcp-remote`](https://www.npmjs.com/package/mcp-remote) bridge:

```json
{"mcpServers": {"sports-odds": {"command": "npx", "args": ["-y", "mcp-remote",
  "https://api.minmaxxxer.dev/mcp",
  "--header", "X-RapidAPI-Key:${RAPIDAPI_KEY}"],
  "env": {"RAPIDAPI_KEY": "YOUR_KEY"}}}}
```

Get a key: subscribe to the [Sports Betting Odds & Arbitrage API](https://minmaxxxer.dev/mcp) on RapidAPI.

## Check it from a terminal

```bash
export RAPIDAPI_KEY=your-key
python examples/check_mcp.py
```

[`examples/check_mcp.py`](examples/check_mcp.py) uses the standard library only. It runs what a client does: `initialize`, `notifications/initialized`, `tools/list` and one `tools/call`.

## Data

- **Leagues:** NBA, NFL, MLB, NHL, ATP and WTA tennis, and 32 soccer leagues (Premier League, LaLiga, Serie A, Bundesliga, Ligue 1, Champions League, MLS and more).
- **History:** soccer since 2005; US leagues and tennis since 2009. About 25 bookmakers per game in current seasons.
- **Pinnacle:** lines recorded every 2 minutes since 22 Oct 2026. Player props for NBA, NFL, NHL, NCAAF, WNBA and MLB.
- **In-play:** Pinnacle only (`get_pinnacle_odds` with `live="true"`), re-read about every 2 minutes; the other bookmakers are pre-match.
- **Analysis only:** the data is for analysis and the server takes no bets. Prices move, so confirm them at the bookmaker.

## Protocol

MCP Streamable HTTP without SSE or sessions:
- one JSON-RPC 2.0 message per POST, answered with `application/json`;
- notifications get `202 Accepted`;
- `GET` answers `405`;
- protocol versions `2026-07-28`, `2025-11-25`, `2025-06-18`, `2025-03-26` and `2024-11-05`.

`server.json` is the entry for the [official MCP Registry](https://registry.modelcontextprotocol.io).

## License

MIT for the code in this repository. The data is served under RapidAPI's terms.
