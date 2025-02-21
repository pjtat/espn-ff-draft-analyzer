import requests
from datetime import datetime
import json
from file_handler import *

# Headers for player requests
X_FANTASY_FILTER = {
            "x-fantasy-filter": json.dumps({
                "players": {
                    "limit": 1500,
                    "sortDraftRanks": {
                        "sortPriority": 100,
                        "sortAsc": True,
                        "value": "STANDARD"
                    }
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
        # Set up logging
        import logging
        import os
        
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.makedirs('logs')
            
        # Configure logging
        self.logger = logging.getLogger('espn_api')
        self.logger.setLevel(logging.DEBUG)
        
        # Create file handler
        fh = logging.FileHandler('logs/espn_api.log')
        fh.setLevel(logging.DEBUG)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        
        # Add handler to logger
        self.logger.addHandler(fh)

    def _make_request(self, season_year, params, additional_headers=None, use_league_endpoint=True):

        # If use_league_endpoint is True, use the league endpoint, otherwise use the players endpoint
        if use_league_endpoint:
            base_url = f'https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{season_year}/segments/0/leagues/{LEAGUE_ID}'
        else:
            base_url = f'https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{season_year}/players'

        try:
            # Log the request URL
            param_str = '&'.join([f"{k}={v}" for k,v in params.items()])
            full_url = f"{base_url}?{param_str}"
            self.logger.info(f"Making request to {full_url}")
            
            # Combine default headers with any passed headers
            request_headers = HEADERS.copy()
            if additional_headers:
                request_headers.update(additional_headers)
                self.logger.debug(f"Using additional headers: {additional_headers}")

            # Send GET request to ESPN API with provided parameters
            response = requests.get(base_url, headers=request_headers, cookies=ESPN_COOKIES, params=params)
            
            # Raise an exception for bad status codes
            response.raise_for_status()
            
            self.logger.info(f"Successfully received response for {params['view']}")

            # Save the response to JSON
            self.file_exporter.save_json_file(f"{params['view']}_{season_year}_response.json", response.json())
            
            # Return the JSON response if successful
            return response.json()
            
        except requests.exceptions.RequestException as e:
            # Log error making request
            self.logger.error(f"Error making request: {e}")
            return None
            
        except ValueError as e:
            # Log JSON parsing error
            self.logger.error(f"Error parsing JSON response: {e}")
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
    
    def get_kona_player_info(self, season_year, scoring_period_id):
        return self._make_request(season_year, {"scoringPeriodId": scoring_period_id, "view": "kona_player_info"}, additional_headers=X_FANTASY_FILTER, use_league_endpoint=True)

    def get_player_wl_info(self, season_year, scoring_period_id):

        return self._make_request(season_year, {"scoringPeriodId": scoring_period_id, "view": "players_wl"}, additional_headers=X_FANTASY_FILTER, use_league_endpoint=True)
    