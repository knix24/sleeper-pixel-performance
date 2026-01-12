# Sleeper Pixel Performance

Visualize your Sleeper fantasy football roster performance with GitHub-style pixel grids.

![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)

## Overview

Track weekly player performance against positional rankings across the season. Density blocks indicate ranking tiers (top 5, top 10, top 15), while blank cells show weeks when players weren't on your roster.

```
              Cleveland Browns - 2025 Season Performance

 Player             1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17
 ─────────────────────────────────────────────────────────────────────
 QB Daniel Jones                ▒  █  ▓  ▓  ░  ▒  ░  ▓  ▒  ░

 QB Lamar Jackson   █  █  █  ░  ░  ░  ░  ░  █  ▒  ░  ░  ░  ▓  ▒  ░  ░

 RB Jahmyr Gibbs    ░  ▓  █  ▒  ▒  ░  █  ░  ░  █  ▒  █  ░  █  ░  ▒  ░


Legend: █ Top 5  ▓ Top 10  ▒ Top 15  ░ Below  · No data
```

## Installation & Usage

**Quick Start** (no installation required):
```bash
./sleeper-pixels <username>
```

**Or install with pip:**
```bash
pip install -e .
sleeper-pixels <username>
```

**Examples:**
```bash
sleeper-pixels angus0024                              # Interactive league selection
sleeper-pixels angus0024 --season 2024 --league ID    # Specify league directly
sleeper-pixels angus0024 -p RB -p WR                  # Filter to specific positions
sleeper-pixels angus0024 --show-points                # Display actual fantasy points
sleeper-pixels angus0024 --html roster.html           # Export to interactive HTML
```

## Options

| Flag | Description |
|------|-------------|
| `--season YEAR` | NFL season year (default: current season) |
| `--league ID` | League ID (prompts if not provided) |
| `--week N` | Max week to display (default: auto-detect from data) |
| `--show-points` | Display fantasy points instead of density symbols |
| `-p, --position POS` | Filter by position (QB, RB, WR, TE, K, DEF); repeatable |
| `--html FILE` | Export to interactive HTML file with hover tooltips |

## Legend

**Terminal symbols:**

| Symbol | Meaning |
|--------|---------|
| █ | Top 5 at position |
| ▓ | Top 6-10 at position |
| ▒ | Top 11-15 at position |
| ░ | Below top 15 |
| · | On roster but no scoring data (bye/injury) |
| _(blank)_ | Not on roster that week |

**HTML export:** Variable cell sizes (larger = better performance) with hover tooltips showing exact points and rank.

## Features

- **Auto-detects scoring weeks** from matchup data
- **Tracks roster tenure** showing exactly when players joined/left your team
- **Position filtering** to focus on specific roles
- **Dual output modes** terminal display or interactive HTML export
- **No authentication** required (uses public Sleeper API)

## Data Source

[Sleeper API](https://docs.sleeper.com)
