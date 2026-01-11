# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Development Commands

```bash
# Run directly (no install needed)
./sleeper-pixels <username>

# Or install with pip
pip install -e .
sleeper-pixels <username>

# Examples
./sleeper-pixels angus0024 --season 2024 --show-points
./sleeper-pixels angus0024 --season 2024 -p RB -p WR
./sleeper-pixels angus0024 --season 2024 --compare
./sleeper-pixels angus0024 --season 2024 --html output.html
```

## CLI Options

- `--season YEAR` - NFL season year (default: current)
- `--league ID` - League ID (prompts if not provided)
- `--week N` - Max week to display (auto-detects from matchup data)
- `--show-points` - Display actual fantasy points instead of symbols
- `-p, --position POS` - Filter by position (QB, RB, WR, TE, K, DEF); repeatable
- `--compare` - Show all teams in league with aggregate weekly performance
- `--html FILE` - Export to HTML file with hover tooltips

## Architecture Overview

Python CLI tool that visualizes fantasy football roster performance using a GitHub-style pixel grid.

**Data Flow:**
1. `cli.py` - Entry point, orchestrates workflow, builds roster tenure data
2. `api.py` - Fetches user, league, roster, and matchup data from Sleeper API
3. `rankings.py` - Calculates weekly positional rankings from matchup scores
4. `grid.py` - Renders pixel grid (terminal via Rich, or HTML export)

**Key Features:**
- Auto-detects weeks with scoring data (doesn't rely on API state)
- Tracks roster tenure from matchup history (shows all players who were ever on roster)
- Blank cells = not on roster; `·` = on roster but no stats; colored = performance tier

**Visualization:**
- Y-axis: Players (sorted by position: QB, RB, WR, TE, K, DEF)
- X-axis: Week numbers
- Colors: bright green (top 5), green (top 10), light green (top 15), gray (below)

## Sleeper API Notes

- Base URL: `https://api.sleeper.app/v1`
- No authentication required
- Rate limit: Stay under 1,000 calls/minute
- Player database (`/players/nfl`) is ~5MB and cached via `@lru_cache`
- Matchups contain `players_points` dict mapping player_id to weekly score
- Roster history derived from weekly matchup `players` arrays
