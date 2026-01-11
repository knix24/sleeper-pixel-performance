"""Sleeper API client."""

import requests
from functools import lru_cache

BASE_URL = "https://api.sleeper.app/v1"


class SleeperAPI:
    """Client for the Sleeper fantasy sports API."""

    def __init__(self):
        self.session = requests.Session()

    def _get(self, endpoint: str) -> dict | list | None:
        """Make a GET request to the Sleeper API."""
        response = self.session.get(f"{BASE_URL}{endpoint}")
        response.raise_for_status()
        return response.json()

    def get_user(self, username: str) -> dict:
        """Get user info by username."""
        return self._get(f"/user/{username}")

    def get_leagues(self, user_id: str, sport: str, season: str) -> list[dict]:
        """Get all leagues for a user in a given sport and season."""
        return self._get(f"/user/{user_id}/leagues/{sport}/{season}")

    def get_league(self, league_id: str) -> dict:
        """Get league details."""
        return self._get(f"/league/{league_id}")

    def get_rosters(self, league_id: str) -> list[dict]:
        """Get all rosters in a league."""
        return self._get(f"/league/{league_id}/rosters")

    def get_users(self, league_id: str) -> list[dict]:
        """Get all users in a league."""
        return self._get(f"/league/{league_id}/users")

    def get_matchups(self, league_id: str, week: int) -> list[dict]:
        """Get matchups for a specific week."""
        return self._get(f"/league/{league_id}/matchups/{week}")

    def get_state(self, sport: str = "nfl") -> dict:
        """Get current state of the sport (week, season, etc.)."""
        return self._get(f"/state/{sport}")

    @lru_cache(maxsize=1)
    def get_players(self, sport: str = "nfl") -> dict:
        """Get all players for a sport. Cached since this is ~5MB."""
        return self._get(f"/players/{sport}")
