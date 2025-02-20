# Import all necessary files for functions below
from espn_api_client import *
from file_exporter import *
from data_cleanup import *

def main(season_year):
    # # Initialize API client and JSON exporter
    api_client = ESPNApiClient()
    file_exporter = FileExporter()
    data_cleanup = DataCleanup()

    # Get the draft results for the given year
    draft_data = api_client.get_draft_details(season_year)

    # Clean up the draft data
    cleaned_draft_data = data_cleanup.clean_up_draft_data(draft_data, season_year) 


if __name__ == "__main__":
    pass