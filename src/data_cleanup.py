from file_exporter import FileExporter

class DataCleanup:
    def __init__(self):
        self.file_exporter = FileExporter()

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
        self.file_exporter.save_json_file(f"{season_year}-draft_results-cleaned.json", cleaned_draft_data)

        return cleaned_draft_data