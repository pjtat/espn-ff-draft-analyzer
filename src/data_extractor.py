from espn_api_client import *
from file_handler import *
from config import LINEUP_SLOT_MAPPING, TEAM_ID_MAPPING

# Extracts and processes data from ESPN Fantasy Football API
class DataExtractor:
    def __init__(self):
        self.api_client = ESPNApiClient()
        self.file_importer = FileImporter()
    def get_league_years(self, current_year):
        # Get the league data
        league_data = self.api_client.get_league_data(current_year)

        # Extract the current season and previous seasons from league data, combine to one list
        current_season = league_data["seasonId"]
        seasons = league_data["status"]["previousSeasons"]
        seasons.append(current_season)

        return seasons
    
    def get_team_information(self, current_year):
        # Get the team data
        team_data = self.api_client.get_team_data(current_year)

        all_team_info = []
        
        # Extract the team names
        for team in team_data["teams"]:
            team_id = team["id"]
            team_name = team["name"]
            team_abbrev = team["abbrev"]
            team_owner_id = team["owners"][0]

            current_team_info = {
                "team_id": team_id,
                "team_name": team_name,
                "team_abbrev": team_abbrev,
                "team_owner_id": team_owner_id
            }

            all_team_info.append(current_team_info)

        # Extract and add the owner names to the team info
        for team in team_data["members"]:
            for team_info in all_team_info:
                if team["id"] == team_info["team_owner_id"]:
                    team_info["team_owner_name"] = team["firstName"] + " " + team["lastName"]

        return all_team_info

    def extract_all_historical_draft_data(self, season_year_list):
        for season_year in season_year_list:
            draft_data = self.api_client.get_draft_details(season_year)

    def extract_all_historical_player_data(self, season_year_list):
        for season_year in season_year_list:
            player_data = self.api_client.get_kona_player_info(season_year, 19)

    def get_player_data(self, season_year, player_ids):
        # Handle single player_id by converting to list
        if isinstance(player_ids, (int, str)):
            player_ids = [int(player_ids)]
        else:
            player_ids = [int(pid) for pid in player_ids]

        # For the given year, pull the player data from the JSON file in the temp files folder
        player_data = self.file_importer.get_json_file(f"kona_player_info_{season_year}_response.json")
        
        # Initialize a list to store the player data
        player_data_list = []

        # For each of the player ids, get the player name, position, team, point total
        for player in player_data["players"]:
            if player["id"] in player_ids:
                player_info = {
                    "player_id": player["id"],
                    "player_name": player["player"]["fullName"],
                    "player_position_id": player["player"]["defaultPositionId"],
                    "player_team_id": player["player"]["proTeamId"],
                    "player_points": player["ratings"]["0"]["totalRating"]
                }
                player_data_list.append(player_info)

        # Determine the player position name and team name
        for player in player_data_list:
            player["player_position_name"] = LINEUP_SLOT_MAPPING[str(player["player_position_id"])]
            player["player_team_name"] = TEAM_ID_MAPPING[str(player["player_team_id"])]

        # If single player_id was passed, return just that player's data
        if isinstance(player_ids, list) and len(player_ids) == 1:
            return player_data_list[0] if player_data_list else None

        return player_data_list