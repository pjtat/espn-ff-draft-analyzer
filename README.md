# ESPN Fantasy Football Analytics

A Python-based analytics tool for extracting and analyzing ESPN Fantasy Football league data. This project helps league managers gather historical draft data, player performance, and team statistics through ESPN's API.

## Features

- For an ESPN Fantasy Football league, determines the best / worst draft picks
- League history extraction and archiving
- Automated data export to JSON files
- Configurable logging system
- Draft pick scoring and ranking system
- Position-specific analysis (QB vs Skill Positions)
- Year-by-year or all-time records

## Prerequisites

- Python 3.x
- `requests` library
- ESPN Fantasy Football League (public or private)
- League manager access for private leagues

## Installation

1. Clone the repository
2. Copy `config.example.py` to `config.py` and configure your league settings
3. Run the script to extract and analyze data

## Usage

1. Run `python src/main.py`
2. Enter a specific year (2000-2100) or 'ALL' for all-time analysis
3. View analysis of best/worst draft picks by position
4. Data is automatically cached in JSON files for future use

## Project Structure

- `src/`
  - `main.py`: Entry point for the application
  - `espn_api_client.py`: Handles API requests to ESPN
  - `data_extractor.py`: Processes and extracts relevant data
  - `file_handler.py`: Manages file I/O operations
  - `config.py`: League-specific configuration
  - `temp files/`: Storage for JSON responses

## Data Storage

All API responses are automatically saved as JSON files in `src/temp files/` for caching and analysis purposes. Files are named according to their view type and season year (e.g., `mTeam_2024_response.json`).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.