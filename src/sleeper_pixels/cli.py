"""Command-line interface for sleeper-pixel-performance."""

import argparse
import sys
from pathlib import Path

from rich.console import Console
from rich.prompt import Prompt

from .api import SleeperAPI
from .grid import export_html, render_pixel_grid
from .rankings import build_roster_performance


def main() -> int:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Visualize fantasy football roster performance with pixel grids"
    )
    parser.add_argument("username", help="Sleeper username")
    parser.add_argument(
        "--season",
        default=None,
        help="NFL season year (default: current season)",
    )
    parser.add_argument(
        "--league",
        default=None,
        help="League ID (will prompt if not provided)",
    )
    parser.add_argument(
        "--week",
        type=int,
        default=None,
        help="Max week to display (default: current week)",
    )
    parser.add_argument(
        "--show-points",
        action="store_true",
        help="Show actual points in each cell instead of symbols",
    )
    parser.add_argument(
        "--position",
        "-p",
        action="append",
        dest="positions",
        choices=["QB", "RB", "WR", "TE", "K", "DEF"],
        help="Filter by position (can specify multiple: -p RB -p WR)",
    )
    parser.add_argument(
        "--html",
        metavar="FILE",
        help="Export to HTML file instead of terminal output",
    )

    args = parser.parse_args()
    console = Console()

    try:
        run(args, console)
        return 0
    except KeyboardInterrupt:
        console.print("\n[yellow]Cancelled.[/yellow]")
        return 1
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        return 1


def run(args: argparse.Namespace, console: Console) -> None:
    """Run the visualization."""
    api = SleeperAPI()

    # Get current state
    console.print("[dim]Fetching NFL state...[/dim]")
    state = api.get_state("nfl")
    current_season = str(state.get("season", "2024"))
    season = args.season or current_season

    # We'll determine max_week after fetching matchups (to find weeks with data)
    requested_week = args.week

    # Get user
    console.print(f"[dim]Looking up user {args.username}...[/dim]")
    user = api.get_user(args.username)
    if not user:
        raise ValueError(f"User '{args.username}' not found")
    user_id = user["user_id"]
    display_name = user.get("display_name", args.username)

    # Get leagues
    console.print(f"[dim]Fetching {season} leagues...[/dim]")
    leagues = api.get_leagues(user_id, "nfl", season)
    if not leagues:
        raise ValueError(f"No NFL leagues found for {season}")

    # Select league
    league_id = args.league
    if not league_id:
        league_id = select_league(leagues, console)

    league = api.get_league(league_id)
    league_name = league.get("name", "Unknown League")

    # Get rosters and users
    console.print("[dim]Fetching rosters...[/dim]")
    rosters = api.get_rosters(league_id)
    users = api.get_users(league_id)

    # Build user_id -> team_name mapping
    user_team_names: dict[str, str] = {}
    for u in users:
        uid = u.get("user_id")
        metadata = u.get("metadata", {})
        team_name = metadata.get("team_name") or u.get("display_name", uid)
        user_team_names[uid] = team_name

    # Fetch matchups for all weeks (up to 17) and detect which have data
    console.print("[dim]Fetching matchups...[/dim]")
    weekly_matchups: dict[int, list[dict]] = {}
    for week in range(1, 18):
        matchups = api.get_matchups(league_id, week)
        # Check if this week has actual scoring data
        has_data = any(
            m.get("players_points") for m in matchups
        ) if matchups else False
        if has_data:
            weekly_matchups[week] = matchups

    # Determine max week from actual data
    if requested_week:
        max_week = requested_week
    elif weekly_matchups:
        max_week = max(weekly_matchups.keys())
    else:
        max_week = 1

    console.print(f"[dim]Found data for weeks 1-{max_week}[/dim]")

    # Get player database
    console.print("[dim]Loading player database...[/dim]")
    players_db = api.get_players("nfl")

    # Build roster_id -> owner_id mapping
    roster_to_owner: dict[int, str] = {}
    owner_to_roster_id: dict[str, int] = {}
    for roster in rosters:
        roster_id = roster.get("roster_id")
        owner_id = roster.get("owner_id")
        if roster_id and owner_id:
            roster_to_owner[roster_id] = owner_id
            owner_to_roster_id[owner_id] = roster_id

    def get_all_season_players(roster_id: int) -> list[str]:
        """Get all players who appeared on a roster throughout the season."""
        all_players: set[str] = set()
        for week_matchups in weekly_matchups.values():
            for matchup in week_matchups:
                if matchup.get("roster_id") == roster_id:
                    players = matchup.get("players") or []
                    all_players.update(players)
        return list(all_players)

    def get_roster_weeks(roster_id: int) -> dict[str, set[int]]:
        """Get which weeks each player was on the roster."""
        player_weeks: dict[str, set[int]] = {}
        for week, week_matchups in weekly_matchups.items():
            for matchup in week_matchups:
                if matchup.get("roster_id") == roster_id:
                    players = matchup.get("players") or []
                    for player_id in players:
                        if player_id not in player_weeks:
                            player_weeks[player_id] = set()
                        player_weeks[player_id].add(week)
        return player_weeks

    # Find user's roster
    user_roster = None
    team_name = display_name
    roster_id = None
    for roster in rosters:
        if roster.get("owner_id") == user_id:
            user_roster = roster
            roster_id = roster.get("roster_id")
            team_name = user_team_names.get(user_id, display_name)
            break

    if not user_roster or not roster_id:
        raise ValueError("Could not find your roster in this league")

    # Get all players from matchup history (not just current roster)
    roster_players = get_all_season_players(roster_id)
    if not roster_players:
        raise ValueError("No player data found in matchups")

    # Get roster membership by week (to show when players joined/left)
    roster_weeks = get_roster_weeks(roster_id)

    # Build performance data (only for weeks player was on roster)
    console.print("[dim]Calculating positional rankings...[/dim]")
    results = build_roster_performance(
        roster_players, weekly_matchups, players_db, max_week, roster_weeks
    )

    if args.html:
        # Export to HTML
        output_path = Path(args.html)
        export_html(
            results,
            team_name,
            season,
            max_week,
            output_path,
            position_filter=args.positions,
            roster_weeks=roster_weeks,
        )
        console.print(f"[green]Exported to {output_path}[/green]")
    else:
        # Render to terminal
        render_pixel_grid(
            results,
            team_name,
            season,
            max_week,
            console,
            show_points=args.show_points,
            position_filter=args.positions,
            roster_weeks=roster_weeks,
        )

    console.print(f"[dim]League: {league_name}[/dim]")


def select_league(leagues: list[dict], console: Console) -> str:
    """Prompt user to select a league."""
    console.print("\n[bold]Select a league:[/bold]")
    for i, league in enumerate(leagues, 1):
        name = league.get("name", "Unknown")
        league_id = league.get("league_id", "")
        console.print(f"  {i}. {name} ({league_id})")

    choice = Prompt.ask(
        "\nEnter number",
        choices=[str(i) for i in range(1, len(leagues) + 1)],
        default="1",
    )
    return leagues[int(choice) - 1]["league_id"]


if __name__ == "__main__":
    sys.exit(main())
