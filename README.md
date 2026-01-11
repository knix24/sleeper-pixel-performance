# Sleeper Pixel Performance

A CLI tool that visualizes your Sleeper fantasy football roster performance using GitHub-style pixel grids.

![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)

## What It Does

Shows how your fantasy players performed each week compared to others at their position. Tracks roster moves throughout the season—blank cells indicate weeks when a player wasn't on your roster.

```
              Cleveland Browns - 2025 Season Performance

 Player             1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17
 ─────────────────────────────────────────────────────────────────────
 QB Daniel Jones             ░  █  █  █  █  ░  █  ░  █  █  ░

 QB Lamar Jackson   █  █  █  ░  ░  ░  ░  ░  █  █  ░  ░  ░  █  █  ░  ░

 RB Jahmyr Gibbs    ░  █  █  █  █  ░  █  ░  ░  █  █  █  ░  █  ░  █  ░

 RB Josh Jacobs     █  ░  ░  █  ░  █  █  ░  █  █  ░  ░  ░  █  █  ░  ░


Legend: █ Top 5  █ Top 10  █ Top 15  ░ Below  · No data
```

## Installation

```bash
# Clone and run directly
./sleeper-pixels <username>

# Or install with pip
pip install -e .
sleeper-pixels <username>
```

## Usage

```bash
# Basic usage - will prompt for league selection
./sleeper-pixels <username>

# Specify season and league
./sleeper-pixels <username> --season 2024 --league <league_id>
```

### Options

| Flag | Description |
|------|-------------|
| `--season YEAR` | NFL season year (default: current) |
| `--league ID` | League ID (prompts if not provided) |
| `--week N` | Max week to display |
| `--show-points` | Show actual fantasy points in cells |
| `-p, --position POS` | Filter by position (QB, RB, WR, TE, K, DEF); repeatable |
| `--compare` | Compare all teams in the league |
| `--html FILE` | Export to HTML with hover tooltips |

### Examples

```bash
# Show only running backs and wide receivers
./sleeper-pixels angus0024 --season 2024 -p RB -p WR

# Display actual points scored
./sleeper-pixels angus0024 --season 2024 --show-points

# Compare all teams in the league
./sleeper-pixels angus0024 --season 2024 --compare

# Export to HTML (includes hover tooltips with exact points/rank)
./sleeper-pixels angus0024 --season 2024 --html roster.html
```

## Reading the Grid

| Symbol | Meaning |
|--------|---------|
| █ (bright) | Top 5 at position that week |
| █ (green) | Top 6-10 at position |
| █ (light) | Top 11-15 at position |
| ░ | Below top 15 |
| · | On roster, but no stats (bye week, injury) |
| _(blank)_ | Not on roster that week |

Blank cells make it easy to see when players were added or dropped throughout the season.

## Data Source

Uses the [Sleeper API](https://docs.sleeper.com) to fetch league, roster, and matchup data. No authentication required.
