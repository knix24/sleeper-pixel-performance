"""Calculate positional rankings from matchup data."""

from collections import defaultdict
from dataclasses import dataclass
from enum import Enum


class Tier(Enum):
    """Performance tier based on positional ranking."""

    ELITE = "elite"  # Top 5
    GREAT = "great"  # Top 6-10
    GOOD = "good"  # Top 11-15
    AVERAGE = "average"  # Below top 15


@dataclass
class PlayerWeekResult:
    """A player's performance for a single week."""

    player_id: str
    player_name: str
    position: str
    week: int
    points: float
    rank: int
    tier: Tier


def get_tier(rank: int) -> Tier:
    """Determine tier based on positional rank."""
    if rank <= 5:
        return Tier.ELITE
    elif rank <= 10:
        return Tier.GREAT
    elif rank <= 15:
        return Tier.GOOD
    else:
        return Tier.AVERAGE


def calculate_weekly_rankings(
    matchups: list[dict],
    players_db: dict,
) -> dict[str, list[tuple[str, float, int, Tier]]]:
    """
    Calculate positional rankings for all players in a week's matchups.

    Returns:
        Dict mapping player_id to (position, points, rank, tier)
    """
    # Collect all player scores grouped by position
    position_scores: dict[str, list[tuple[str, float]]] = defaultdict(list)

    for matchup in matchups:
        players_points = matchup.get("players_points", {})
        if not players_points:
            continue

        for player_id, points in players_points.items():
            if player_id not in players_db:
                continue
            player_info = players_db[player_id]
            position = player_info.get("position", "UNKNOWN")
            if position in ("QB", "RB", "WR", "TE", "K", "DEF"):
                position_scores[position].append((player_id, points or 0))

    # Rank players within each position
    player_rankings: dict[str, tuple[str, float, int, Tier]] = {}

    for position, scores in position_scores.items():
        # Sort by points descending
        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)

        for rank, (player_id, points) in enumerate(sorted_scores, start=1):
            tier = get_tier(rank)
            player_rankings[player_id] = (position, points, rank, tier)

    return player_rankings


def build_roster_performance(
    roster_players: list[str],
    weekly_matchups: dict[int, list[dict]],
    players_db: dict,
    max_week: int,
) -> list[PlayerWeekResult]:
    """
    Build performance data for all players on a roster across all weeks.

    Args:
        roster_players: List of player IDs on the roster
        weekly_matchups: Dict mapping week number to matchup data
        players_db: Full player database
        max_week: Maximum week number to process

    Returns:
        List of PlayerWeekResult for each player/week combination
    """
    results = []

    for week in range(1, max_week + 1):
        matchups = weekly_matchups.get(week, [])
        if not matchups:
            continue

        rankings = calculate_weekly_rankings(matchups, players_db)

        for player_id in roster_players:
            if player_id not in players_db:
                continue

            player_info = players_db[player_id]
            player_name = player_info.get("full_name") or player_info.get(
                "last_name", player_id
            )
            position = player_info.get("position", "UNKNOWN")

            if player_id in rankings:
                pos, points, rank, tier = rankings[player_id]
                results.append(
                    PlayerWeekResult(
                        player_id=player_id,
                        player_name=player_name,
                        position=position,
                        week=week,
                        points=points,
                        rank=rank,
                        tier=tier,
                    )
                )

    return results
