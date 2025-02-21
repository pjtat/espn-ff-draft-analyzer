# Import all necessary files for functions below
from espn_api_client import *
from data_extractor import *
from file_handler import *

def main(season_year):
    # # Initialize API client and JSON exporter
    api_client = ESPNApiClient()
    data_extractor = DataExtractor()
    file_importer = FileImporter()

    # Determine the league years
    league_years = data_extractor.get_league_years(season_year)

    # Extract all of the draft data and player data
    data_extractor.extract_all_historical_draft_data(league_years)
    data_extractor.extract_all_historical_player_data(league_years)

    # Pull in the draft data for the given year
    draft_data = file_importer.get_json_file(f"mDraftDetail_{season_year}_response.json")
    draft_picks = draft_data["draftDetail"]["picks"]

    # Remove all keepers from the draft picks list
    draft_picks = [pick for pick in draft_picks if pick["keeper"] == False]

    # For each of the draft picks, add the player name, position, team, point total
    for draft_pick in draft_picks:
        player_data = data_extractor.get_player_data(season_year, draft_pick["playerId"])
        draft_pick["player_name"] = player_data["player_name"]
        draft_pick["player_position_name"] = player_data["player_position_name"]
        draft_pick["player_team_name"] = player_data["player_team_name"]
        draft_pick["player_points"] = player_data["player_points"]
    
    # Sort the draft picks by the player_points field
    draft_picks.sort(key=lambda x: x["player_points"], reverse=True)

    # Add a ranking value to each of the draft picks
    for i, draft_pick in enumerate(draft_picks):
        draft_pick["overall_point_ranking"] = i + 1
    
    # Determine the "draft_score" which is the initial draft position of the player 
    # minus the "overall_point_ranking"
    for draft_pick in draft_picks:
        draft_pick["draft_score"] = draft_pick["overallPickNumber"] - draft_pick["overall_point_ranking"]
    
    # Get top/bottom 5 draft scores for QBs
    qb_picks = [pick for pick in draft_picks if pick["player_position_name"] == "QB"]
    skill_picks = [pick for pick in draft_picks if pick["player_position_name"] in ["WR", "RB", "TE"]]

    # QB top/bottom 5
    bottom_5_qbs = sorted(qb_picks, key=lambda x: x["draft_score"])[:5] 
    top_5_qbs = sorted(qb_picks, key=lambda x: x["draft_score"], reverse=True)[:5]

    # Skill position top/bottom 10
    bottom_10_skill = sorted(skill_picks, key=lambda x: x["draft_score"])[:10]
    top_10_skill = sorted(skill_picks, key=lambda x: x["draft_score"], reverse=True)[:10]

    # Get team information
    team_data = data_extractor.get_team_information(season_year)

    # Add the owner name to all positional lists
    for position_list in [bottom_5_qbs, top_5_qbs, bottom_10_skill, top_10_skill]:
        for draft_pick in position_list:
            for team in team_data:
                if draft_pick["teamId"] == team["team_id"]:
                    draft_pick["owner_name"] = team["team_owner_name"]
                    break

    # Create a dictionary to store all results
    draft_results = {
        'quarterbacks': {
            'best': top_5_qbs,
            'worst': bottom_5_qbs
        },
        'skill_positions': {
            'best': top_10_skill,
            'worst': bottom_10_skill
        }
    }

    print("\nTop 5 Best QB Draft Picks:")
    print("---------------------------")
    for pick in top_5_qbs:
        print(f"Player: {pick['player_name']} ({pick['player_position_name']} - {pick['player_team_name']})")
        print(f"Drafted: Round {pick['roundId']}, Pick {pick['roundPickNumber']} (#{pick['overallPickNumber']} overall)")
        print(f"Points: {pick['player_points']:.1f}")
        print(f"Point Ranking: #{pick['overall_point_ranking']}")
        print(f"Draft Score: {pick['draft_score']}")
        print(f"Owner: {pick['owner_name']}")
        print()

    print("\nTop 5 Worst QB Draft Picks:")
    print("----------------------------")
    for pick in bottom_5_qbs:
        print(f"Player: {pick['player_name']} ({pick['player_position_name']} - {pick['player_team_name']})")
        print(f"Drafted: Round {pick['roundId']}, Pick {pick['roundPickNumber']} (#{pick['overallPickNumber']} overall)")
        print(f"Points: {pick['player_points']:.1f}")
        print(f"Point Ranking: #{pick['overall_point_ranking']}")
        print(f"Draft Score: {pick['draft_score']}")
        print(f"Owner: {pick['owner_name']}")
        print()

    print("\nTop 10 Best Skill Position Draft Picks:")
    print("---------------------------------------")
    for pick in top_10_skill:
        print(f"Player: {pick['player_name']} ({pick['player_position_name']} - {pick['player_team_name']})")
        print(f"Drafted: Round {pick['roundId']}, Pick {pick['roundPickNumber']} (#{pick['overallPickNumber']} overall)")
        print(f"Points: {pick['player_points']:.1f}")
        print(f"Point Ranking: #{pick['overall_point_ranking']}")
        print(f"Draft Score: {pick['draft_score']}")
        print(f"Owner: {pick['owner_name']}")
        print()

    print("\nTop 10 Worst Skill Position Draft Picks:")
    print("----------------------------------------")
    for pick in bottom_10_skill:
        print(f"Player: {pick['player_name']} ({pick['player_position_name']} - {pick['player_team_name']})")
        print(f"Drafted: Round {pick['roundId']}, Pick {pick['roundPickNumber']} (#{pick['overallPickNumber']} overall)")
        print(f"Points: {pick['player_points']:.1f}")
        print(f"Point Ranking: #{pick['overall_point_ranking']}")
        print(f"Draft Score: {pick['draft_score']}")
        print(f"Owner: {pick['owner_name']}")
        print()

    return draft_results

if __name__ == "__main__":
    # Modify the main execution to capture results if needed
    while True:
        choice = input("Enter the season year (e.g. 2024) or 'ALL' for all-time rankings: ").strip().upper()
        
        if choice == 'ALL':
            # Determine league years
            data_extractor = DataExtractor()
            league_years = data_extractor.get_league_years(2024)

            all_results = {}

            # Compile the results from each year, then create an all time list for best/worsts
            for year in league_years:
                try:
                    results = main(year)
                except Exception as e:
                    print(f"Error processing year {year}: {str(e)}")
                    continue
                # Add the year to each of the picks included in the results
                for position in ['quarterbacks', 'skill_positions']:
                    for pick in results[position]['best']:
                        pick['year'] = year
                    for pick in results[position]['worst']:
                        pick['year'] = year
                
                all_results[year] = results
                
                # Create an all time list for best/worsts
                all_time_results = {
                    'quarterbacks': {
                        'best': [],
                        'worst': []
                    },
                    'skill_positions': {
                        'best': [],
                        'worst': []
                    }
                }
                
                # Add the best/worst picks from each year to the all time list
                for year, results in all_results.items():
                    all_time_results['quarterbacks']['best'].extend(results['quarterbacks']['best'])
                    all_time_results['quarterbacks']['worst'].extend(results['quarterbacks']['worst'])
                    all_time_results['skill_positions']['best'].extend(results['skill_positions']['best'])
                    all_time_results['skill_positions']['worst'].extend(results['skill_positions']['worst'])
                
                # Sort the all time list by draft score (best = highest score, worst = lowest score)
                all_time_results['quarterbacks']['best'].sort(key=lambda x: x['draft_score'], reverse=True)
                all_time_results['quarterbacks']['worst'].sort(key=lambda x: x['draft_score'])
                all_time_results['skill_positions']['best'].sort(key=lambda x: x['draft_score'], reverse=True)
                all_time_results['skill_positions']['worst'].sort(key=lambda x: x['draft_score'])
                
                # Print the all time list
                print("\nAll Time Best QB Draft Picks:")
                print("----------------------------")
                for pick in all_time_results['quarterbacks']['best'][:5]:
                    print(f"Player: {pick['player_name']} ({pick['player_position_name']} - {pick['player_team_name']})")
                    print(f"Year: {pick['year']}")
                    print(f"Drafted: Round {pick['roundId']}, Pick {pick['roundPickNumber']} (#{pick['overallPickNumber']} overall)")
                    print(f"Points: {pick['player_points']:.1f}")
                    print(f"Point Ranking: #{pick['overall_point_ranking']}")
                    print(f"Draft Score: {pick['draft_score']}")
                    print(f"Owner: {pick['owner_name']}")
                    print()
                
                print("\nAll Time Worst QB Draft Picks:")
                print("----------------------------")
                for pick in all_time_results['quarterbacks']['worst'][:5]:
                    print(f"Player: {pick['player_name']} ({pick['player_position_name']} - {pick['player_team_name']})")
                    print(f"Year: {pick['year']}")
                    print(f"Drafted: Round {pick['roundId']}, Pick {pick['roundPickNumber']} (#{pick['overallPickNumber']} overall)")
                    print(f"Points: {pick['player_points']:.1f}")
                    print(f"Point Ranking: #{pick['overall_point_ranking']}")
                    print(f"Draft Score: {pick['draft_score']}")
                    print(f"Owner: {pick['owner_name']}")
                    print()

                print("\nAll Time Best Skill Position Draft Picks:")
                print("---------------------------------------")
                for pick in all_time_results['skill_positions']['best'][:10]:
                    print(f"Player: {pick['player_name']} ({pick['player_position_name']} - {pick['player_team_name']})")
                    print(f"Year: {pick['year']}")
                    print(f"Drafted: Round {pick['roundId']}, Pick {pick['roundPickNumber']} (#{pick['overallPickNumber']} overall)")
                    print(f"Points: {pick['player_points']:.1f}")
                    print(f"Point Ranking: #{pick['overall_point_ranking']}")
                    print(f"Draft Score: {pick['draft_score']}")
                    print(f"Owner: {pick['owner_name']}")
                    print()

                print("\nAll Time Worst Skill Position Draft Picks:")
                print("----------------------------------------")
                for pick in all_time_results['skill_positions']['worst'][:10]:
                    print(f"Player: {pick['player_name']} ({pick['player_position_name']} - {pick['player_team_name']})")
                    print(f"Year: {pick['year']}")
                    print(f"Drafted: Round {pick['roundId']}, Pick {pick['roundPickNumber']} (#{pick['overallPickNumber']} overall)")
                    print(f"Points: {pick['player_points']:.1f}")
                    print(f"Point Ranking: #{pick['overall_point_ranking']}")
                    print(f"Draft Score: {pick['draft_score']}")
                    print(f"Owner: {pick['owner_name']}")
                    print()
            break
            
        else:
            try:
                season_year = int(choice)
                if 2000 <= season_year <= 2100:
                    results = main(season_year)
                    break
                else:
                    print("Please enter a valid year.")
            except ValueError:
                print("Please enter a valid year or 'ALL'")