# Sleeper Pixel Performance

A CLI tool that visualizes your Sleeper fantasy football roster performance using GitHub-style pixel grids.

![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)

## What It Does

Shows how your fantasy players performed each week compared to others at their position:

```
              Cleveland Browns - 2024 Season Performance
┏━━━━━━━━━━━━━━━━━━┳━━┳━━┳━━┳━━┳━━┳━━┳━━┳━━┳━━┳━━┳━━┳━━┳━━┳━━┳━━┳━━┳━━┓
┃Player            ┃1 ┃2 ┃3 ┃4 ┃5 ┃6 ┃7 ┃8 ┃9 ┃10┃11┃12┃13┃14┃15┃16┃17┃
┡━━━━━━━━━━━━━━━━━━╇━━╇━━╇━━╇━━╇━━╇━━╇━━╇━━╇━━╇━━╇━━╇━━╇━━╇━━╇━━╇━━╇━━┩
│QB Lamar Jackson  │█ │█ │█ │█ │█ │█ │█ │█ │█ │█ │░ │█ │█ │░ │█ │█ │█ │
│                  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │
│RB Jahmyr Gibbs   │░ │█ │█ │█ │░ │░ │█ │█ │░ │░ │█ │█ │░ │█ │█ │█ │█ │
│RB Josh Jacobs    │░ │░ │░ │░ │█ │░ │█ │█ │░ │░ │█ │█ │█ │█ │█ │█ │█ │
└──────────────────┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘

Legend: █ Top 5  █ Top 10  █ Top 15  ░ Below  · No data
```

## Installation

```bash
pip install -e .
```

## Usage

```bash
# Basic usage - will prompt for league selection
sleeper-pixels <username>

# Specify season and league
sleeper-pixels <username> --season 2024 --league <league_id>
```

### Options

| Flag | Description |
|------|-------------|
| `--season YEAR` | NFL season year (default: current) |
| `--league ID` | League ID (prompts if not provided) |
| `--week N` | Max week to display |
| `--show-points` | Show actual fantasy points in cells |
| `-p, --position POS` | Filter by position (QB, RB, WR, TE, K, DEF) |
| `--compare` | Compare all teams in the league |
| `--html FILE` | Export to HTML with hover tooltips |

### Examples

```bash
# Show only running backs and wide receivers
sleeper-pixels angus0024 --season 2024 -p RB -p WR

# Display actual points scored
sleeper-pixels angus0024 --season 2024 --show-points

# Compare all teams in the league
sleeper-pixels angus0024 --season 2024 --compare

# Export to HTML (includes hover tooltips with exact points/rank)
sleeper-pixels angus0024 --season 2024 --html roster.html
```

## Color Key

| Color | Meaning |
|-------|---------|
| Dark green | Top 5 at position |
| Green | Top 6-10 at position |
| Light green | Top 11-15 at position |
| Gray | Below top 15 |

## Data Source

Uses the [Sleeper API](https://docs.sleeper.com) to fetch league, roster, and matchup data. No authentication required.
