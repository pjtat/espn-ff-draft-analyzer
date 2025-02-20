import requests
from datetime import datetime
import json
from file_exporter import FileExporter

# Headers for player requests
X_FANTASY_FILTER = {
            "x-fantasy-filter": json.dumps({
                "players": {
                    "limit": 1200
                }
            })
        }
# X_FANTASY_FILTER = {
#             "x-fantasy-filter": json.dumps({
#                 "players": {
#                     "filterStatsForExternalIds": {"value": [season_year]},  # Use provided season year
#                     "filterSlotIds": {"value": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 19]},
#                     "filterStatsForSourceIds": {"value": [0, 1]},
#                     "useFullProjectionTable": {"value": True},
#                     "sortAppliedStatTotal": {"sortAsc": False, "sortPriority": 2, "value": "102020"},
#                     "sortDraftRanks": {"sortPriority": 3, "sortAsc": True, "value": "STANDARD"},
#                     "sortPercOwned": {"sortPriority": 4, "sortAsc": False},
#                     "limit": 1200,
#                     "offset": 0,  # Start from the first record
#                     "filterStatsForTopScoringPeriodIds": {
#                         "value": 5,
#                         "additionalValue": ["002020", "102020", "012020", "022020", "032020", "042020", "010002020"]
#                     }
#                 }
#             })
#         }

# Bring in variables needed for API requests 
from config import LEAGUE_ID, ESPN_COOKIES, HEADERS

class ESPNApiClient:
    def __init__(self):
        self.file_exporter = FileExporter()

    def _make_request(self, season_year, params, additional_headers=None):
        try:
            # Construct the URL with the provided season year
            url = f'https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{season_year}/segments/0/leagues/{LEAGUE_ID}'
            
            # Combine default headers with any passed headers
            request_headers = HEADERS.copy()
            if additional_headers:
                request_headers.update(additional_headers)

            # Send GET request to ESPN API with provided parameters
            response = requests.get(url, headers=request_headers, cookies=ESPN_COOKIES, params=params)
            # Raise an exception for bad status codes
            response.raise_for_status()
            # Print the response to JSON
            self.file_exporter.save_json_file(f"{params['view']}_response.json", response.json())
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
    
    def get_team_data(self, season_year):
        # Fetch team data for the league
        return self._make_request(season_year, {"view": "mTeam"})
    
    def get_league_data(self, season_year):
        # Fetch team data for the league
        return self._make_request(season_year, {"view": "mNav"})

    def get_league_settings(self, season_year):
        # Fetch league settings for the league
        return self._make_request(season_year, {"view": "mSettings"})
    
    def get_draft_details(self, season_year):
        # Fetch draft details for the league
        return self._make_request(season_year, {"view": "mDraftDetail", "seasonId": season_year})
    
    def get_kona_player_info(self, season_year):

        return self._make_request(season_year, {"view": "kona_player_info"}, X_FANTASY_FILTER)

    def get_player_wl_info(self, season_year):

        return self._make_request(season_year, {"view": "players_wl"}, X_FANTASY_FILTER)
    