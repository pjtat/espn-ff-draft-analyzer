import requests
from datetime import datetime
import json
from file_exporter import FileExporter

# Bring in variables needed for API requests 
from config import LEAGUE_ID, ESPN_COOKIES, HEADERS, LEAGUE_YEAR

class ESPNApiClient:
    def __init__(self):
        self.file_exporter = FileExporter()

        # Figure out the current year in order to construct the base URL
        current_year = LEAGUE_YEAR

        # Construct the base URL for ESPN Fantasy Football API requests
        self.base_url = f'https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{current_year}/segments/0/leagues/{LEAGUE_ID}'

    def _make_request(self, params, headers=None):
        try:
            # Combine default headers with any passed headers
            request_headers = HEADERS.copy()
            if headers:
                request_headers.update(headers)

            # Send GET request to ESPN API with provided parameters
            response = requests.get(self.base_url, headers=request_headers, cookies=ESPN_COOKIES, params=params)
            # Raise an exception for bad status codes
            response.raise_for_status()
            # Return the JSON response if successful
            return response.json()
        except requests.exceptions.RequestException as e:
            # Report error making request
            print(f"Error making request: {e}")
            return None
        except ValueError as e:
            # Report JSON parsing error
            print(f"Error parsing JSON response: {e}")
            return None
    
    def get_team_data(self):
        # Fetch team data for the league
        return self._make_request({"view": "mTeam"})
    
    def get_league_data(self):
        # Fetch team data for the league
        return self._make_request({"view": "mNav"})

    def get_league_settings(self):
        # Fetch league settings for the league
        return self._make_request({"view": "mSettings"})
    
    def get_draft_details(self, season_id):
        # Fetch draft details for the league
        return self._make_request({"view": "mDraftDetail", "seasonId": season_id})
    
    def get_kona_player_info(self, ):
        headers = {
            "x-fantasy-filter": json.dumps({
                "players": {
                    "filterStatsForExternalIds": {"value": [2020]},  # Only 2020 stats
                    "filterSlotIds": {"value": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 19]},
                    "filterStatsForSourceIds": {"value": [0, 1]},
                    "useFullProjectionTable": {"value": True},
                    "sortAppliedStatTotal": {"sortAsc": False, "sortPriority": 2, "value": "102020"},
                    "sortDraftRanks": {"sortPriority": 3, "sortAsc": True, "value": "STANDARD"},
                    "sortPercOwned": {"sortPriority": 4, "sortAsc": False},
                    "limit": 1200,
                    "offset": 0,  # Start from the first record
                    "filterStatsForTopScoringPeriodIds": {
                        "value": 5,
                        "additionalValue": ["002020", "102020", "012020", "022020", "032020", "042020", "010002020"]
                    }
                }
            })
        }
    
        return self._make_request({"view": "kona_player_info"}, headers)

    def get_player_wl_info(self):
        headers = {
            "x-fantasy-filter": json.dumps({
                "players": {
                    "filterStatsForExternalIds": {"value": [2020]},  # Only 2020 stats
                    "filterSlotIds": {"value": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 19]},
                    "filterStatsForSourceIds": {"value": [0, 1]},
                    "useFullProjectionTable": {"value": True},
                    "sortAppliedStatTotal": {"sortAsc": False, "sortPriority": 2, "value": "102020"},
                    "sortDraftRanks": {"sortPriority": 3, "sortAsc": True, "value": "STANDARD"},
                    "sortPercOwned": {"sortPriority": 4, "sortAsc": False},
                    "limit": 1200,
                    "offset": 0,  # Start from the first record
                    "filterStatsForTopScoringPeriodIds": {
                        "value": 5,
                        "additionalValue": ["002020", "102020", "012020", "022020", "032020", "042020", "010002020"]
                    }
                }
            })
        }

        return self._make_request({"view": "players_wl"}, headers)
    