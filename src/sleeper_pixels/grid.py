"""Terminal pixel grid visualization."""

from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich.text import Text

from .rankings import PlayerWeekResult, Tier

# Rich terminal colors - more vibrant
TIER_COLORS = {
    Tier.ELITE: "bold bright_green",  # Bright green - Top 5
    Tier.GREAT: "green",  # Green - Top 6-10
    Tier.GOOD: "dark_sea_green2",  # Light green - Top 11-15
    Tier.AVERAGE: "bright_black",  # Dim gray - Below top 15
}

# HTML colors (GitHub contribution graph style)
TIER_HTML_COLORS = {
    Tier.ELITE: "#216e39",  # Dark green - Top 5
    Tier.GREAT: "#30a14e",  # Green - Top 6-10
    Tier.GOOD: "#9be9a8",  # Light green - Top 11-15
    Tier.AVERAGE: "#ebedf0",  # Off white - Below top 15
    None: "#f6f8fa",  # No data
}

TIER_SYMBOLS = {
    Tier.ELITE: "█",
    Tier.GREAT: "█",
    Tier.GOOD: "█",
    Tier.AVERAGE: "░",
}


def render_pixel_grid(
    results: list[PlayerWeekResult],
    team_name: str,
    season: str,
    max_week: int,
    console: Console | None = None,
    show_points: bool = False,
    position_filter: list[str] | None = None,
    roster_weeks: dict[str, set[int]] | None = None,
) -> None:
    """
    Render a GitHub-style pixel grid showing roster performance.

    Y-axis: Players (grouped by position)
    X-axis: Week numbers
    Color: Performance tier at position

    Args:
        roster_weeks: Optional dict mapping player_id to set of weeks they were on roster.
                      Used to distinguish "not on roster" (blank) from "on roster, no data" (·)
    """
    if console is None:
        console = Console()

    # Group results by player
    player_weeks: dict[str, dict[int, PlayerWeekResult]] = {}
    player_info: dict[str, tuple[str, str]] = {}  # player_id -> (name, position)

    for result in results:
        if result.player_id not in player_weeks:
            player_weeks[result.player_id] = {}
            player_info[result.player_id] = (result.player_name, result.position)
        player_weeks[result.player_id][result.week] = result

    if not player_weeks:
        console.print("[yellow]No performance data found for this roster.[/yellow]")
        return

    # Filter by position if specified
    if position_filter:
        position_filter_upper = [p.upper() for p in position_filter]
        player_info = {
            pid: info
            for pid, info in player_info.items()
            if info[1] in position_filter_upper
        }

    # Sort players by position then name
    position_order = {"QB": 0, "RB": 1, "WR": 2, "TE": 3, "K": 4, "DEF": 5}
    sorted_players = sorted(
        player_info.items(),
        key=lambda x: (position_order.get(x[1][1], 99), x[1][0]),
    )

    # Build the table with horizontal lines between rows
    from rich.box import SIMPLE_HEAD

    table = Table(
        title=f"{team_name} - {season} Season Performance",
        show_header=True,
        header_style="bold",
        show_lines=True,
        padding=(0, 0),
        box=SIMPLE_HEAD,
    )

    # Add player column
    table.add_column("Player", style="cyan", no_wrap=True, min_width=18)

    # Add week columns (wider if showing points)
    col_width = 5 if show_points else 2
    for week in range(1, max_week + 1):
        table.add_column(str(week), justify="center", width=col_width)

    # Add rows for each player
    for player_id, (name, position) in sorted_players:
        # Build the row
        row = [f"[dim]{position}[/dim] {name[:15]}"]

        weeks_data = player_weeks.get(player_id, {})
        player_roster_weeks = roster_weeks.get(player_id, set()) if roster_weeks else None
        for week in range(1, max_week + 1):
            if week in weeks_data:
                result = weeks_data[week]
                color = TIER_COLORS[result.tier]
                symbol = TIER_SYMBOLS[result.tier]
                if show_points:
                    pts = f"{result.points:.0f}"
                    row.append(f"[{color}]{pts:>4}[/{color}]")
                else:
                    row.append(f"[{color}]{symbol}[/{color}]")
            elif player_roster_weeks is None or week in player_roster_weeks:
                # On roster but no scoring data (bye week, injury, etc.)
                row.append("[dim]·[/dim]")
            else:
                # Not on roster this week
                row.append(" ")

        table.add_row(*row)

    console.print()
    console.print(table)
    console.print()

    # Print legend
    render_legend(console)


def render_legend(console: Console) -> None:
    """Render the color legend."""
    legend = Text("Legend: ")
    legend.append("█", style=TIER_COLORS[Tier.ELITE])
    legend.append(" Top 5  ")
    legend.append("█", style=TIER_COLORS[Tier.GREAT])
    legend.append(" Top 10  ")
    legend.append("█", style=TIER_COLORS[Tier.GOOD])
    legend.append(" Top 15  ")
    legend.append("░", style=TIER_COLORS[Tier.AVERAGE])
    legend.append(" Below  ")
    legend.append("·", style="dim")
    legend.append(" No data")

    console.print(legend)
    console.print()


def export_html(
    results: list[PlayerWeekResult],
    team_name: str,
    season: str,
    max_week: int,
    output_path: Path,
    position_filter: list[str] | None = None,
    roster_weeks: dict[str, set[int]] | None = None,
) -> None:
    """Export the pixel grid as an HTML file with proper CSS colors."""
    # Group results by player
    player_weeks: dict[str, dict[int, PlayerWeekResult]] = {}
    player_info: dict[str, tuple[str, str]] = {}

    for result in results:
        if result.player_id not in player_weeks:
            player_weeks[result.player_id] = {}
            player_info[result.player_id] = (result.player_name, result.position)
        player_weeks[result.player_id][result.week] = result

    # Filter by position if specified
    if position_filter:
        position_filter_upper = [p.upper() for p in position_filter]
        player_info = {
            pid: info
            for pid, info in player_info.items()
            if info[1] in position_filter_upper
        }

    # Sort players
    position_order = {"QB": 0, "RB": 1, "WR": 2, "TE": 3, "K": 4, "DEF": 5}
    sorted_players = sorted(
        player_info.items(),
        key=lambda x: (position_order.get(x[1][1], 99), x[1][0]),
    )

    # Build HTML
    html_parts = [
        """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{team_name} - {season} Season Performance</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
            background: #0d1117;
            color: #c9d1d9;
            padding: 20px;
        }}
        h1 {{
            font-size: 24px;
            margin-bottom: 20px;
        }}
        .grid-container {{
            display: inline-block;
            background: #161b22;
            border-radius: 6px;
            padding: 16px;
        }}
        table {{
            border-collapse: collapse;
        }}
        th, td {{
            padding: 2px;
            text-align: center;
            font-size: 12px;
        }}
        th {{
            color: #8b949e;
            font-weight: normal;
            padding-bottom: 8px;
        }}
        .player-name {{
            text-align: left;
            padding-right: 12px;
            white-space: nowrap;
        }}
        .position {{
            color: #8b949e;
            margin-right: 4px;
        }}
        .cell {{
            width: 14px;
            height: 14px;
            border-radius: 2px;
            margin: 1px;
            display: inline-block;
            cursor: pointer;
        }}
        .cell:hover {{
            outline: 1px solid #58a6ff;
        }}
        .spacer-row td {{
            height: 8px;
        }}
        .legend {{
            margin-top: 16px;
            font-size: 12px;
        }}
        .legend-item {{
            display: inline-flex;
            align-items: center;
            margin-right: 16px;
        }}
        .legend-box {{
            width: 12px;
            height: 12px;
            border-radius: 2px;
            margin-right: 4px;
        }}
        .tooltip {{
            position: relative;
        }}
        .tooltip:hover::after {{
            content: attr(data-tooltip);
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            background: #1f2428;
            color: #c9d1d9;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 11px;
            white-space: nowrap;
            z-index: 100;
            border: 1px solid #30363d;
        }}
    </style>
</head>
<body>
    <h1>{team_name} - {season} Season Performance</h1>
    <div class="grid-container">
        <table>
            <thead>
                <tr>
                    <th class="player-name">Player</th>
""".format(
            team_name=team_name, season=season
        )
    ]

    # Week headers
    for week in range(1, max_week + 1):
        html_parts.append(f'                    <th>{week}</th>\n')
    html_parts.append("                </tr>\n            </thead>\n            <tbody>\n")

    # Player rows
    current_position = None
    for player_id, (name, position) in sorted_players:
        # Add spacer row between positions
        if current_position is not None and position != current_position:
            html_parts.append(
                f'                <tr class="spacer-row"><td colspan="{max_week + 1}"></td></tr>\n'
            )
        current_position = position

        html_parts.append("                <tr>\n")
        html_parts.append(
            f'                    <td class="player-name"><span class="position">{position}</span>{name}</td>\n'
        )

        weeks_data = player_weeks.get(player_id, {})
        player_roster_weeks = roster_weeks.get(player_id, set()) if roster_weeks else None
        for week in range(1, max_week + 1):
            if week in weeks_data:
                result = weeks_data[week]
                color = TIER_HTML_COLORS[result.tier]
                tooltip = f"Week {week}: {result.points:.1f} pts (#{result.rank} {position})"
                html_parts.append(
                    f'                    <td><div class="cell tooltip" style="background-color: {color};" data-tooltip="{tooltip}"></div></td>\n'
                )
            elif player_roster_weeks is None or week in player_roster_weeks:
                # On roster but no scoring data
                color = TIER_HTML_COLORS[None]
                html_parts.append(
                    f'                    <td><div class="cell" style="background-color: {color};"></div></td>\n'
                )
            else:
                # Not on roster - empty cell
                html_parts.append(
                    '                    <td></td>\n'
                )

        html_parts.append("                </tr>\n")

    # Close table and add legend
    html_parts.append(
        """            </tbody>
        </table>
    </div>
    <div class="legend">
        <span class="legend-item"><span class="legend-box" style="background-color: {elite};"></span>Top 5</span>
        <span class="legend-item"><span class="legend-box" style="background-color: {great};"></span>Top 10</span>
        <span class="legend-item"><span class="legend-box" style="background-color: {good};"></span>Top 15</span>
        <span class="legend-item"><span class="legend-box" style="background-color: {avg};"></span>Below</span>
        <span class="legend-item"><span class="legend-box" style="background-color: {none};"></span>No data</span>
    </div>
</body>
</html>
""".format(
            elite=TIER_HTML_COLORS[Tier.ELITE],
            great=TIER_HTML_COLORS[Tier.GREAT],
            good=TIER_HTML_COLORS[Tier.GOOD],
            avg=TIER_HTML_COLORS[Tier.AVERAGE],
            none=TIER_HTML_COLORS[None],
        )
    )

    output_path.write_text("".join(html_parts))


def render_compare_grid(
    all_team_results: dict[str, list[PlayerWeekResult]],
    season: str,
    max_week: int,
    console: Console | None = None,
    position_filter: list[str] | None = None,
) -> None:
    """
    Render a summary grid comparing all teams in a league.

    Shows aggregate performance for each team by week.
    """
    if console is None:
        console = Console()

    table = Table(
        title=f"League Comparison - {season} Season",
        show_header=True,
        header_style="bold",
        padding=(0, 0),
    )

    table.add_column("Team", style="cyan", no_wrap=True, min_width=20)
    for week in range(1, max_week + 1):
        table.add_column(str(week), justify="center", width=2)
    table.add_column("Avg", justify="center", width=4, style="bold")

    for team_name, results in sorted(all_team_results.items()):
        # Filter by position if specified
        if position_filter:
            position_filter_upper = [p.upper() for p in position_filter]
            results = [r for r in results if r.position in position_filter_upper]

        # Calculate weekly averages
        weekly_scores: dict[int, list[float]] = {w: [] for w in range(1, max_week + 1)}
        for result in results:
            if result.rank <= 15:  # Only count top-15 finishes
                weekly_scores[result.week].append(result.rank)

        row = [team_name[:18]]
        season_ranks = []

        for week in range(1, max_week + 1):
            ranks = weekly_scores[week]
            if ranks:
                avg_rank = sum(ranks) / len(ranks)
                season_ranks.extend(ranks)
                tier = (
                    Tier.ELITE
                    if avg_rank <= 5
                    else Tier.GREAT
                    if avg_rank <= 10
                    else Tier.GOOD
                    if avg_rank <= 15
                    else Tier.AVERAGE
                )
                color = TIER_COLORS[tier]
                row.append(f"[{color}]█[/{color}]")
            else:
                row.append("[dim]·[/dim]")

        # Season average
        if season_ranks:
            avg = sum(season_ranks) / len(season_ranks)
            row.append(f"{avg:.1f}")
        else:
            row.append("-")

        table.add_row(*row)

    console.print()
    console.print(table)
    console.print()
    render_legend(console)
