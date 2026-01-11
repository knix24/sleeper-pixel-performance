# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Development Commands

```bash
# Install dependencies
pip install -e .

# Run the tool
sleeper-pixels <username>
sleeper-pixels <username> --season 2024 --league <league_id>

# Run directly without installing
python -m sleeper_pixels.cli <username>

# Examples with options
sleeper-pixels angus0024 --season 2024 --show-points        # Show actual points
sleeper-pixels angus0024 --season 2024 -p RB -p WR          # Filter positions
sleeper-pixels angus0024 --season 2024 --compare            # Compare all teams
sleeper-pixels angus0024 --season 2024 --html output.html   # Export to HTML
```

## CLI Options

- `--season YEAR` - NFL season year (default: current)
- `--league ID` - League ID (prompts if not provided)
- `--week N` - Max week to display (default: 17 for past seasons)
- `--show-points` - Display actual fantasy points instead of symbols
- `-p, --position POS` - Filter by position (QB, RB, WR, TE, K, DEF); can specify multiple
- `--compare` - Show all teams in league with aggregate weekly performance
- `--html FILE` - Export to HTML file with GitHub-style colors and hover tooltips

## Architecture Overview

Python CLI tool that visualizes fantasy football roster performance using a GitHub-style pixel grid.

**Data Flow:**
1. `cli.py` - Entry point, orchestrates the workflow and handles all CLI flags
2. `api.py` - Fetches user, league, roster, and matchup data from Sleeper API
3. `rankings.py` - Calculates weekly positional rankings from matchup scores
4. `grid.py` - Renders pixel grid (terminal via Rich, or HTML export)

**Visualization Logic:**
- Y-axis: Players on roster (grouped by position: QB, RB, WR, TE, K, DEF)
- X-axis: Week numbers
- Colors based on positional ranking that week:
  - Dark green (#216e39): Top 5 at position
  - Green (#30a14e): Top 6-10
  - Light green (#9be9a8): Top 11-15
  - Gray (#ebedf0): Below top 15

## Sleeper API Notes

- Base URL: `https://api.sleeper.app/v1`
- No authentication required
- Rate limit: Stay under 1,000 calls/minute
- Player database (`/players/nfl`) is ~5MB and cached via `@lru_cache`
- Matchups contain `players_points` dict mapping player_id to weekly score
- Rankings are calculated against all rostered players in the league for that week
