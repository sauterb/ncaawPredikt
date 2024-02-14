# CSCI 5922 Final Project
# Bailey Sauter, Fall 2023

import numpy as np
import requests
import json
from NN_models import RNN_model

# Global variables for API calls
access_level = 'trial'
version = 'v8'
language_code = 'en'
ncaawb_season_type = 'REG'
format = 'json'

# Custom class for storing team information
class teamSeason:
    def __init__(self, name):
        self.name = name
        self.games = []
        self.current_game_set = False
        self.next_game = None
        self.next_game_percentage = None

    def add_game(self, game):
        self.games.append(game)

    def reset_for_this_year(self, snapshot_length):
        self.games = []
        self.wins_bool = np.zeros(snapshot_length)
        self.margins = np.zeros(snapshot_length)
        self.home_bool = np.zeros(snapshot_length)
        self.point_differential = np.zeros(snapshot_length)
        self.opponent_rpi = np.zeros(snapshot_length)
        self.self_rpi = np.zeros(snapshot_length)

    def parse_all_games(self, rpi_data):
        num_games = len(self.games)
        self.wins_bool = np.zeros(num_games)
        self.margins = np.zeros(num_games)
        self.home_bool = np.zeros(num_games)
        self.point_differential = np.zeros(num_games)
        self.opponent_rpi = np.zeros(num_games)

        # Get team's own ranking and store as sequence
        for ranking in rpi_data['rankings']:
            if ranking['name'] in self.name and ranking['market'] in self.name:
                self.self_rpi = np.asarray([ranking['rank'] for game in self.games])

        # Iterate over games in a season and extract feature arrays
        for i,game in enumerate(self.games):
            if game['status'] == 'closed':
                self.point_differential[i] = sum(self.margins) / (i + 1)
            if game['home']['name'] == self.name:
                if game['status'] == 'closed':
                    self.margins[i] = game['home_points']-game['away_points']
                self.home_bool[i] = 1
                for ranking in rpi_data['rankings']:
                    if ranking['name'] in game['away']['name'] and ranking['market'] in game['away']['name']:
                        self.opponent_rpi[i] = ranking['rank']
            elif game['away']['name'] == self.name:
                if game['status'] == 'closed':
                    self.margins[i] = -game['home_points']+game['away_points']
                self.home_bool[i] = 0
                for ranking in rpi_data['rankings']:
                    if ranking['name'] in game['home']['name'] and ranking['market'] in game['home']['name']:
                        self.opponent_rpi[i] = ranking['rank']
            if self.opponent_rpi[i] == 0:
                # If opponent not found in RPI, assume very bad
                self.opponent_rpi[i] = 300
            if game['status'] == 'closed':
                if self.margins[i] < 0:
                    self.wins_bool[i] = 0
                else:
                    self.wins_bool[i] = 1

# List of teams used in this project (Power 5)
team_list = [
    teamSeason("Colorado Buffaloes"),
    teamSeason("Washington State Cougars"),
    teamSeason("Washington Huskies"),
    teamSeason("Oregon State Beavers"),
    teamSeason("Oregon Ducks"),
    teamSeason("Stanford Cardinal"),
    teamSeason("California Golden Bears"),
    teamSeason("USC Trojans"),
    teamSeason("UCLA Bruins"),
    teamSeason("Arizona State Sun Devils"),
    teamSeason("Arizona Wildcats"),
    teamSeason("Utah Utes"),
    teamSeason("Michigan Wolverines"),
    teamSeason("Ohio State Buckeyes"),
    teamSeason("Penn State Lady Lions"),
    teamSeason("Maryland Terrapins"),
    teamSeason("Rutgers Scarlet Knights"),
    teamSeason("Michigan State Spartans"),
    teamSeason("Indiana Hoosiers"),
    teamSeason("Iowa Hawkeyes"),
    teamSeason("Northwestern Wildcats"),
    teamSeason("Wisconsin Badgers"),
    teamSeason("Nebraska Cornhuskers"),
    teamSeason("Minnesota Golden Gophers"),
    teamSeason("Illinois Fighting Illini"),
    teamSeason("Purdue Boilermakers"),
    teamSeason("Baylor Bears"),
    teamSeason("BYU Cougars"),
    teamSeason("UCF Knights"),
    teamSeason("Cincinnati Bearcats"),
    teamSeason("Houston Cougars"),
    teamSeason("Iowa State Cyclones"),
    teamSeason("Kansas Jayhawks"),
    teamSeason("Kansas State Wildcats"),
    teamSeason("Oklahoma Sooners"),
    teamSeason("Oklahoma State Cowgirls"),
    teamSeason("TCU Horned Frogs"),
    teamSeason("Texas Longhorns"),
    teamSeason("Texas Tech Lady Raiders"),
    teamSeason("West Virginia Mountaineers"),
    teamSeason("Alabama Crimson Tide"),
    teamSeason("Arkansas Razorbacks"),
    teamSeason("Auburn Tigers"),
    teamSeason("Florida Gators"),
    teamSeason("Georgia Lady Bulldogs"),
    teamSeason("Kentucky Wildcats"),
    teamSeason("LSU Lady Tigers"),
    teamSeason("Ole Miss Rebels"),
    teamSeason("Mississippi State Lady Bulldogs"),
    teamSeason("Missouri Tigers"),
    teamSeason("South Carolina Gamecocks"),
    teamSeason("Tennessee Lady Volunteers"),
    teamSeason("Vanderbilt Commodores"),
    teamSeason("Boston College Eagles"),
    teamSeason("Duke Blue Devils"),
    teamSeason("Florida State Seminoles"),
    teamSeason("Georgia Tech Yellow Jackets"),
    teamSeason("Louisville Cardinals"),
    teamSeason("Miami (FL) Hurricanes"),
    teamSeason("North Carolina Tar Heels"),
    teamSeason("North Carolina State Wolfpack"),
    teamSeason("Notre Dame Fighting Irish"),
    teamSeason("Pittsburgh Panthers"),
    teamSeason("Syracuse Orange"),
    teamSeason("Virginia Cavaliers"),
    teamSeason("Virginia Tech Hokies"),
    teamSeason("Wake Forest Demon Deacons")
]

# Use API to fetch NCAAW season data
def get_NCAAW_season_data(file_saveName, yyyy):

    year = yyyy

    api_url = f"https://api.sportradar.com/ncaawb/{access_level}/{version}/{language_code}" \
              f"/seasons/{year}/{ncaawb_season_type}/standings.{format}?api_key=7fv6azmbwjbjb64c2dqbd88w"

    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()

        with open(file_saveName + '.json', 'w') as json_file:
            print(f"Successs! Saved API response to {file_saveName}.json")
            json.dump(data, json_file)
    else:
        print("Error:", response.status_code, response.text)

# Use API to fetch NCAAW RPI data
def get_NCAAW_RPI_data(file_saveName:str, yyyy):
    api_url = f"https://api.sportradar.com/ncaawb/{access_level}/{version}/{language_code}" \
              f"/rpi/{yyyy}/rankings.{format}?api_key=7fv6azmbwjbjb64c2dqbd88w"

    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()

        with open(file_saveName + '.json', 'w') as json_file:
            print(f"Successs! Saved API response to {file_saveName}.json")
            json.dump(data, json_file)
    else:
        print("Error:", response.status_code, response.text)

# Use API to fetch NCAAW scheduling data
def get_NCAAW_schedule(file_saveName:str, yyyy):
    season_year = yyyy

    api_url = f"https://api.sportradar.com/ncaawb/{access_level}/{version}/{language_code}" \
              f"/games/{season_year}/{ncaawb_season_type}/schedule.{format}?api_key=7fv6azmbwjbjb64c2dqbd88w"

    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()

        with open(file_saveName + '.json', 'w') as json_file:
            print(f"Successs! Saved API response to {file_saveName}.json")
            json.dump(data, json_file)
    else:
        print("Error:", response.status_code, response.text)

# Used to extract the X and y vectors used to train the model
def clean_and_prepare_data():
    use_api = False

    year = "2022"
    if use_api:
        print("Using one API")
        get_NCAAW_season_data(f"ncaaw_season_{year}", year)
        get_NCAAW_schedule(f"ncaaw_schedule_{year}", year)
        get_NCAAW_RPI_data(f"ncaaw_rpi_{year}", year)

    # Load json
    with open(f"ncaaw_season_{year}.json", 'r') as json_file:
        ncaaw_season_data = json.load(json_file)
    with open(f"ncaaw_schedule_{year}.json", 'r') as json_file:
        ncaaw_schedule_data = json.load(json_file)
    with open(f"ncaaw_rpi_{year}.json", 'r') as json_file:
        ncaaw_rpi_data = json.load(json_file)

    for game in ncaaw_schedule_data['games']:
        for team in team_list:
            if game['home']['name'] == team.name or game['away']['name'] == team.name:
                # Limit games to 27 per team to generate homogenous arrays
                if game['status'] == 'closed' and len(team.games) < 27:
                    team.add_game(game)

    for team in team_list:
        team.parse_all_games(ncaaw_rpi_data)

    # Features and labels arrays
    X = list([])
    y = list([])

    # Sequences must be homogoneous, so this checks that teams are all capped to same length of season
    uniform_num_games = min([len(team.games) for team in team_list])

    # Extracts features as sequences of games over the course of the season
    snapshot_length = 7
    stride_length = 5
    for team in team_list:
        if len(team.games) == 0:
            print(team.name, "has 0 games (name probably wrong)")
        for i in range(1,uniform_num_games-snapshot_length,stride_length):
            X.append([team.home_bool[i:i+snapshot_length],
                      team.self_rpi[i:i+snapshot_length],
                      team.opponent_rpi[i:i+snapshot_length],
                      team.wins_bool[i-1:i+snapshot_length-1],
                      team.point_differential[i-1:i+snapshot_length-1],
                      ])
            y.append(team.wins_bool[i:i+snapshot_length])

    X = np.asarray(X)
    X = np.swapaxes(X,1,2)
    y = np.asarray(y)
    return X,y

# Gets team information and cleans data for current year to make live predictions
def get_current_year(use_API:bool):
    # Boolean tells whether to refresh the API (if teams have played more games, e.g.)
    use_api = use_API

    year = "2023"
    if use_api:
        print("Using one API")
        get_NCAAW_season_data(f"ncaaw_season_{year}", year)
        get_NCAAW_schedule(f"ncaaw_schedule_{year}", year)
        get_NCAAW_RPI_data(f"ncaaw_rpi_{year}", year)

    # Load json
    with open(f"ncaaw_season_{year}.json", 'r') as json_file:
        ncaaw_season_data = json.load(json_file)
    with open(f"ncaaw_schedule_{year}.json", 'r') as json_file:
        ncaaw_schedule_data = json.load(json_file)
    with open(f"ncaaw_rpi_{year}.json", 'r') as json_file:
        ncaaw_rpi_data = json.load(json_file)

    for team in team_list:
        team.reset_for_this_year(snapshot_length=10)
        team.current_game_set = False

    for game in ncaaw_schedule_data['games']:
        for team in team_list:
            if (game['home']['name'] == team.name or game['away']['name'] == team.name) and team.current_game_set == False:
                if game['status'] == 'closed':
                    team.add_game(game)
                elif game['status'] == 'scheduled':
                    team.add_game(game)
                    team.current_game_set = True
                    team.next_game = game

    for team in team_list:
        team.parse_all_games(ncaaw_rpi_data)

    X = list([])

    uniform_num_games = min([len(team.games) for team in team_list])

    snapshot_length = 7
    for team in team_list:
        num_games = len(team.games)
        X.append([team.home_bool[num_games - snapshot_length:num_games - snapshot_length + snapshot_length],
                  team.self_rpi[num_games - snapshot_length:num_games - snapshot_length + snapshot_length],
                  team.opponent_rpi[num_games - snapshot_length:num_games - snapshot_length + snapshot_length],
                  team.wins_bool[num_games - snapshot_length - 1:num_games - snapshot_length + snapshot_length - 1],
                  team.point_differential[num_games - snapshot_length - 1:num_games - snapshot_length + snapshot_length - 1],
                  ])

    X = np.asarray(X)
    X = np.swapaxes(X, 1, 2)
    return X

def percent_to_moneyline(percent):
    decimal = percent/100.0
    multiplier = "+"

    if decimal > .5:
        multiplier = "-"
        decimal = 1-decimal

    moneyline = 100/decimal - 100
    moneyline = round(moneyline, 0)

    return multiplier + str(moneyline)

# Make predictions for current season
def make_predictions(X, model):
    predictions = model.predict(X, batch_size=32, use_multiprocessing=True, verbose=True)
    final_predictions = np.round(100 * np.asarray([sequence[-1][0] for sequence in predictions]),decimals=1)

    # Make dictionary of upcoming games that website can reference
    upcoming_games = {}

    # Clamp each game prediction and output the correctly formatted text
    for i,team in enumerate(team_list):
        team.next_game_percentage = final_predictions[i]
        # No such thing as a guarantee
        if team.next_game_percentage > 99.9:
            team.next_game_percentage = 99.9
        elif team.next_game_percentage < 0.1:
            team.next_game_percentage = 0.1
        foo = str(team.next_game_percentage)
        if team.next_game_percentage > 50:
            color='green'
        elif team.next_game_percentage < 50:
            color='red'
        upcoming_games[team.name] = (f"\n\n\n\n**{team.name}**, next game: \n\n{team.next_game['away']['name']} vs. {team.next_game['home']['name']}"
                           f"\n\nWill take place on {team.next_game['scheduled'][5:7]}/{team.next_game['scheduled'][8:10]}/{team.next_game['scheduled'][0:4]} at {team.next_game['scheduled'][11:19]} in {team.next_game['venue']['city']}, {team.next_game['venue']['state']}"
                           f"\n\n:rainbow[NNostradamus] predicts The {team.name} have a **:{color}[{foo}%]** chance of winning"
                           f"\n\nPredicted moneyline = {percent_to_moneyline(team.next_game_percentage)}, bet if moneyline higher")

    # print(upcoming_games)
    return upcoming_games

# This only needs run to update the model, otherwise Streamlit project will access saved model
if __name__ == '__main__':
    # ---Data Analysis Section---
    X, y = clean_and_prepare_data()
    ncaaw_model = RNN_model(X, y)
    ncaaw_model.save('ncaaw_model.keras')