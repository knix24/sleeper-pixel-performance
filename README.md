# Sleeper Pixel Performance

Visualize your Sleeper fantasy football roster performance with GitHub-style pixel grids.

![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)

## What It Does

Shows weekly player performance compared to others at their position. Density blocks indicate ranking tier; blank cells show weeks when a player wasn't on your roster.

```
              Cleveland Browns - 2025 Season Performance

 Player             1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17
 ─────────────────────────────────────────────────────────────────────
 QB Daniel Jones                ▒  █  ▓  ▓  ░  ▒  ░  ▓  ▒  ░

 QB Lamar Jackson   █  █  █  ░  ░  ░  ░  ░  █  ▒  ░  ░  ░  ▓  ▒  ░  ░

 RB Jahmyr Gibbs    ░  ▓  █  ▒  ▒  ░  █  ░  ░  █  ▒  █  ░  █  ░  ▒  ░


Legend: █ Top 5  ▓ Top 10  ▒ Top 15  ░ Below  · No data
```

## Installation

```bash
./sleeper-pixels <username>          # Run directly
pip install -e . && sleeper-pixels   # Or install first
```

## Usage

```bash
./sleeper-pixels <username>                              # Prompts for league
./sleeper-pixels <username> --season 2024 --league ID    # Specify league
./sleeper-pixels <username> -p RB -p WR                  # Filter positions
./sleeper-pixels <username> --show-points                # Show actual points
./sleeper-pixels <username> --html roster.html           # Export to HTML
```

### Options

| Flag | Description |
|------|-------------|
| `--season YEAR` | NFL season year (default: current) |
| `--league ID` | League ID (prompts if not provided) |
| `--week N` | Max week to display |
| `--show-points` | Show fantasy points instead of symbols |
| `-p, --position` | Filter by position (QB, RB, WR, TE, K, DEF) |
| `--html FILE` | Export HTML with hover tooltips |

## Reading the Grid

| Symbol | Meaning |
|--------|---------|
| █ | Top 5 at position |
| ▓ | Top 6-10 |
| ▒ | Top 11-15 |
| ░ | Below top 15 |
| · | On roster, no stats (bye/injury) |
| _(blank)_ | Not on roster |

**HTML export:** Cell size varies by tier (larger = better performance). Hover for exact points and rank.

## Data Source

[Sleeper API](https://docs.sleeper.com) — no authentication required.
