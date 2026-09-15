# Scouting Schedules
A simple tool for creating minimal scouting schedules using the TBA API for use in the FIRST Robotics Competition.

For each match with the target team:
Returns the latest, previous match of every other team in the current match.

## Usage
All values you need are at the top of the python file, including the event key, the team key, and the TBA API key. Run the program and it will generate a minimal schedule for you.

Set the required values:
- Your team key
- Event key
- TBA API key

### Running the script
- Create a Virtual Environment: `python3 -m venv .venv`
- Activate the Virtual Environment: `source .venv/bin/activate` or `.\.venv\Scripts\Activate.ps1`
- Install `requests`: `python3 -m pip install requests`
- Run the python file: `python3 main.py`

Output is saved to a file in the format `{event_key}_schedule.csv`
