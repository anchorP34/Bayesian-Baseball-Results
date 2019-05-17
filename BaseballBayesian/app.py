# Bring in the imports
import argparse
from head_to_head import head_to_head, get_home_bayesain_prob, get_away_bayesain_prob
import pandas as pd
from datetime import datetime
import json


def load_season(season, start_date, end_date):
    """
    Description: Loads all head to head games based on the season year, start date and end date
    Input: season (string) - Year of the baseball season
           start_date (string) - yyyymmdd format. Will only work if games were played on that day
           end_date (string) - yyyymmdd format. Will only work if games were played on that day
    Output: YYYY Season Results (JSON) - JSON format of game results for each team
            YYYY Head to Head (CSV) - CSV file for all head to head matchups and the bayesian probability of each one
    """
    try:
        season_games = pd.read_csv('{} Head To Head.csv'.format(season))
        with open('{} Season Results.json'.format(season), 'r') as f:
            season_dict = json.load(f)
        
        # If there is no start season, then just take the most recent date
        if start_date is None:
            start_date = season_games['Date'].max()
        # If there are no more games to load since the last time it was loaded
        if start_date == datetime.today().strftime('%Y-%m-%d'):
            print('You are already all up to date')
            quit()
        else:
            start_date = start_date.replace('-','')

        new_games_dict, new_games_df = head_to_head([season], season_dict, start_date, end_date)

        season_games.append(new_games_df, ignore_index = True).to_csv('{} Head To Head.csv'.format(season), index = False)

        with open("{} Season Results.json".format(season),"w") as f:
            json.dump(new_games_dict,f)
        
    # If there is no loaded games yet for the specific season
    except FileNotFoundError:
        print('Files for the {} season were not found, so creating them now'.format(season))
        new_games_dict, new_games_df = head_to_head([season], None, start_date, end_date)

        new_games_df.to_csv('{} Head To Head.csv'.format(season), index = False)

        with open("{} Season Results.json".format(season),"w") as f:
            json.dump(new_games_dict,f)

        print('Files have been successfully created')



def get_matchup(home_team, away_team, season):
    """
    Description: Gets the probability of the home team and away team of a season
    Input: home_team (string) : Home Team of the baseball game
           away_team (string) : Away Team of the baseball game
           season (string) : Baseball season of reference
    Output: Printed values of the probabilities of winning according to bayesian theory
    """
    try:
        with open('{} Season Results.json'.format(season), 'r') as f:
            season_dict = json.load(f)
        

        home_team_dict = season_dict[season][home_team]
        away_team_dict = season_dict[season][away_team]

        home_bayesian_prob = get_home_bayesain_prob(
                    home_team_dict['TotalWins'] 
                    , home_team_dict['TotalLosses'] 
                    , home_team_dict['HomeWins'] 
                    , home_team_dict['HomeLosses'] 
                )
        away_bayesian_prob = get_home_bayesain_prob(
                    away_team_dict['TotalWins'] 
                    , away_team_dict['TotalLosses'] 
                    , away_team_dict['AwayWins'] 
                    , away_team_dict['AwayLosses'] 
                )

        print("{} -- Winning Probability: {}%".format(away_team, round(100 * (away_bayesian_prob / (home_bayesian_prob + away_bayesian_prob)), 2)))
        print("{} -- Winning Probability: {}%".format(home_team, round(100 * (home_bayesian_prob / (home_bayesian_prob + away_bayesian_prob)), 2)))
        

    except FileNotFoundError:
        print("""It doesn't look like you have the current season games loaded. Run this command first to load the season:
            python: python app.py --season 2019
            docker: docker run -v "$(pwd)":/app  bayesian-baseball --season 2019
        """)

now = datetime.today()

parser = argparse.ArgumentParser(description='This program is to get Bayesian MLB predictions')

parser.add_argument("--season"
                    ,help = "Season of interest.")
parser.add_argument("--startDate"
                    , default = None
                    ,help = 'Date to start pulling results (must be date when games were actually played)')
parser.add_argument("--endDate"
                    , default = None
                    ,help = "Last date of game results (must be date when games were actually played)")

parser.add_argument("--HomeTeam"
                    , help = "Home Team of the matchup"
                )
parser.add_argument("--AwayTeam"
                    , help = "Away Team of the matchup"
                )

args = parser.parse_args()

if args.season is None:
    args.season = str(now.year)
else:
    load_season(args.season, args.startDate, args.endDate)
    print("{} has been fully loaded".format(args.season))

if args.HomeTeam is not None and args.AwayTeam is not None:
    get_matchup(args.HomeTeam, args.AwayTeam, args.season)







