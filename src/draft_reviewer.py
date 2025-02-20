from espn_api_client import ESPNApiClient
from file_exporter import FileExporter
import json

class DraftReviewer:
    def __init__(self):
        self.api_client = ESPNApiClient()
        self.file_exporter = FileExporter()

    def get_draft_results(self, season_year):
        # Get draft data from ESPN API
        draft_data = self.api_client.get_draft_details(season_year)
        
        # Save draft data to JSON file
        self.file_exporter.save_json_file("mDraftDetail_API_response.json", draft_data)

        return draft_data
    
    def clean_up_draft_data(self, draft_data, season_year):
        # Initialize a new dictionary to store the cleaned up data
        cleaned_draft_data = []

        # Reconfigure the data to be more readable with draft picks listed in order beneath team id
        for pick in draft_data['draftDetail']['picks']:
            team_id = pick['teamId']
            draft_pick_round = pick['roundId']
            draft_pick_number = pick['roundPickNumber']
            overall_pick_number = pick['overallPickNumber']
            player_id = pick['playerId']
            keeper = pick['keeper']

            # Store only the data above in the same order as the original data
            cleaned_draft_data.append({
                'team_id': team_id,
                'draft_pick_round': draft_pick_round,
                'draft_pick_number': draft_pick_number,
                'overall_pick_number': overall_pick_number,
                'player_id': player_id,
                'keeper': keeper
            })

        # Create a new JSON file with the cleaned up data
        self.file_exporter.save_json_file(f"draft_results-{season_year}.json", cleaned_draft_data)

        return cleaned_draft_data

    def determine_draft_pick_scores(self, draft_data):
        # Draft pick 
        pass

    def get_player_yearly_scores(self):
        # Convert the filter dictionary to a JSON string
        player_info = self.api_client.get_player_info()
        
        # Save to temp file
        self.file_exporter.save_json_file("temp.json", player_info)

if __name__ == "__main__":
    draft_reviewer = DraftReviewer()
    # draft_data = draft_reviewer.get_draft_results(2023)
    # draft_reviewer.clean_up_draft_data(draft_data, 2023)
    draft_reviewer.get_player_yearly_scores()