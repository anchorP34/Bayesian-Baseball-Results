import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re


import warnings
warnings.filterwarnings("ignore")

def get_home_bayesain_prob(total_wins, total_losses, home_wins, home_losses):
    """
    Description:
        Calculating the Bayesian probability that given the team wins, what is the probability
        that they were the home team
        
        P(W|H) = Probability you win, given you're at home
        P(H|W) = Probability you're at home, given you won
        P(W) = Probability you win
        P(H|L) = Probability you're at home, given you lost 
        P(L) = Probability that you lost

        P(W|H) = ( P(H|W) * P(W) ) / ( P(H|W) * P(W) + P(H|L) * P(L) )

    Output:
        Bayesian Prob - Float

    """

    if home_wins + home_losses == 0:
        return np.nan
    else:
        home_win_pct = (home_wins) / (home_wins + home_losses)
        home_losing_pct = 1 - home_win_pct

        overall_win_pct = (total_wins) / (total_wins + total_losses)
        overall_losing_pct = 1 - overall_win_pct

        numerator = (home_win_pct * overall_win_pct) 
        denominator = ((home_win_pct * overall_win_pct) + (home_losing_pct * overall_losing_pct))

        if denominator == 0:
            bayesian_prob = 0
        else:
            bayesian_prob = numerator / denominator

        return bayesian_prob

def get_away_bayesain_prob(total_wins, total_losses, away_wins, away_losses):
    """
    Description:
        Calculating the Bayesian probability that given the team wins, what is the probability
        that they were the away team
        
        P(W|A) = Probability you win, given you're away
        P(A|W) = Probability you're away, given you won
        P(W) = Probability you win
        P(A|L) = Probability you're away, given you lost 
        P(L) = Probability that you lost

        P(W|A) = ( P(A|W) * P(W) ) / ( P(A|W) * P(W) + P(A|L) * P(L) )

    Output:
        Bayesian Prob - Float

    """

    if away_wins + away_losses == 0:
        return np.nan
    else:
        away_win_pct = (away_wins) / (away_wins + away_losses)
        away_losing_pct = 1 - away_win_pct

        overall_win_pct = (total_wins) / (total_wins + total_losses)
        overall_losing_pct = 1 - overall_win_pct

        numerator = (away_win_pct * overall_win_pct) 
        denominator = ((away_win_pct * overall_win_pct) + (away_losing_pct * overall_losing_pct))

        if denominator == 0:
            bayesian_prob = 0
        else:
            bayesian_prob = numerator / denominator

        return bayesian_prob

def correct_prediction(row):
    """
    Description: See if the projected winner by Bayesian statistics was the actual winner of the game

    Returns: 1, 0, NULL (Yes, No, Not Available)
    """
    home_team = row['HomeTeam']
    away_team = row['AwayTeam']

    winning_team = row['WinningTeam']

    home_win_prob = row['HomeWinningProb']
    away_win_prob = row['AwayWinningProb']

    # If either team has a blank probability, then dont calulate it
    if pd.isnull(home_win_prob) or pd.isnull(away_win_prob):
        return np.nan
    # If both teams have a 50/50 shot, then there was no clear winner 
    elif home_win_prob == away_win_prob:
        return np.nan 
    # If the home team has a higher probability and was the winning team, then correct
    elif home_win_prob > away_win_prob and home_team == winning_team:
        return 1
    # If the away team has a higher probability and was the winning team, then correct
    elif home_win_prob < away_win_prob and away_team == winning_team:
        return 1
    # If none of the above are true, then it must have been a incorrect prediction
    else:
        return 0



def head_to_head(seasons, all_seasons_dict, start_date, end_date):
    """
    Description: 
        Pulling every inning of every game from the input season from https://www.baseball-reference.com
    
    INPUT: 
        Season (string) - The season of the MLB year you would like to pull
        all_seasons_dict (dictionary) - If there has already been games loaded, this will make things faster
        end_date (string) - Date of the first game that you would like to pull
                       Example: If you would like to skip the season until the month of May,
                       put '20170501' for start_date
                       *** Note: Games must be played on the start date for this to work ***
        end_date (string) - Date of the last game that you would like to pull 
                       Example: If the playoffs in the 2017 season start  October 3, 2017, you want that 
                       to be the stop date. So, for end_date, you would put '20171003' as the stop date.
    
    OUTPUT: 
        all_seasons_dict (dictionary) - Shows the following information about the season for each team
            TotalWins - Total Wins
            TotalLosses - Total Losses
            HomeWins - Number of wins that occured when playing at home
            AwayWins - Number of wins that occured when playing on the road
            HomeLosses - Number of losses that occured when playing at home
            AwayLosses - Number of losses that occured when playing on the road
            TotalGameOutcomes - Array of W's and L's of each game played throughout the year, 
                                along with whether they were home (H) or away (A)
            HomeGameOutcomes - Array of W's and L's of each home game played throughout the year
            AwayGameOutcomes - Array of W's and L's of each away game played throughout the year

        all_seasons_df (DataFrame) - Shows the following information about each matchup:
            Season - Year teh game was played
            Date - Date of the game
            HomeTeam - Home Team
            AwayTeam - Away Team
            HomeTeamTotalWins - Total wins on the season of the home team
            HomeTeamTotalLosses - Total losses on the season of the home team
            AwayTeamTotalWins - Total wins on the season of the away team
            AwayTeamTotalLosses - Total losses on the season the of away team
            HomeTeamHomeWins - Total number of home wins for the home team on the year
            HomeTeamHomeLosses - Total number of home losses for the home team on the year
            AwayTeamHomeWins - Total number of away wins for the away team on the year
            AwayTeamHomeWins - Total number of away wins for the away team on the year
            HomeTeamBayesianWinningProb - The bayesian winning probability of the home team winning at home
            AwayTeamBayesianWinningProb - The bayesian winning probability of the away team winning on the road
            HomeWinningProb - The overall winning probability of the home team
            AwayWinningProb - The overall winning probability of the away team
            WinningTeam - Team who won the matchup
            CorrectPrediction - Was the bayesian matchup correct?
  
    """

    if all_seasons_dict is None:
        all_seasons_dict = {}
        

    for season in seasons:
        season = str(season)
        if season not in all_seasons_dict:
            all_seasons_dict[season] = {}
        
        all_seasons_df = pd.DataFrame(columns = ['Season','Date','HomeTeam','AwayTeam'
                                                , 'HomeTeamTotalWins', 'HomeTeamTotalLosses'
                                                , 'AwayTeamTotalWins', 'AwayTeamTotalLosses'
                                                , 'HomeTeamHomeWins','HomeTeamHomeLosses'
                                                , 'AwayTeamAwayWins','AwayTeamAwayLosses'
                                                , 'HomeTeamBayesianWinningProb','AwayTeamBayesianWinningProb'
                                                , 'HomeWinningProb','AwayWinningProb'
                                                , 'WinningTeam'
                                                ]
                                    )

        season_request = requests.get('https://www.baseball-reference.com/leagues/MLB/{}-schedule.shtml'.format(season))
        season_soup = BeautifulSoup(season_request.text, 'lxml')

        all_season_games = [list(elem.parent.attrs.values())[0] for elem in season_soup(text=re.compile('Boxscore'))]

        game_idx = 0
        if start_date is not None:
            for game_num, game in enumerate(all_season_games):
                if start_date in game:
                    game_idx = game_num
                    

        all_season_games = all_season_games[game_idx+1:]

        if all_season_games == []:
            print('No games left to load at this time')
            quit()
        
        for game_html in all_season_games:
            print('https://www.baseball-reference.com' + game_html)
            
            if end_date is not None and end_date in game_html:
                break
            else:

                game_request = requests.get('https://www.baseball-reference.com' + game_html)
                game_soup = BeautifulSoup(game_request.text, 'lxml')

                away_team = game_soup.find(attrs = {"class":"linescore_wrap"}).find('tbody').find_all('a')[2].string
                home_team = game_soup.find(attrs = {"class":"linescore_wrap"}).find('tbody').find_all('a')[-1].string

                for team in [away_team, home_team]:
                # Add teams to dictionary if they don't exist
                    if team not in all_seasons_dict[season]:
                        all_seasons_dict[season][team] = {
                                                            'TotalWins' : 0
                                                            , 'TotalLosses' : 0

                                                            , 'HomeWins': 0
                                                            , 'AwayWins': 0

                                                            , 'HomeLosses': 0
                                                            , 'AwayLosses': 0

                                                            , 'TotalGameOutcomes': []
                                                            , 'HomeGameOutcomes': []
                                                            , 'AwayGameOutcomes' : []
                                                        }


                game_boxscore = []
                for x in game_soup.find(attrs = {"class":"linescore_wrap"}).find('tbody').find_all(attrs = {"class": "center"}):
                    if '<div class="media-item logo loader">' not in str(x):
                        game_boxscore.append(x.text)

                date = game_html.split('.shtml')[0][-9:-1]
                date_format = date[0:4] + '-' + date[4:6] + '-' + date[6:]
                print(date_format)
                away_box = game_boxscore[: int(len(game_boxscore) / 2)]
                home_box = game_boxscore[int(len(game_boxscore) / 2):] 

                # Hold just in case want to work with total runs for a game
                away_score = away_box[-3]
                home_score = home_box[-3]


                # Get Bayesian Probabilities
                home_bayesian_prob = get_home_bayesain_prob(
                    all_seasons_dict[season][home_team]['TotalWins'] 
                    , all_seasons_dict[season][home_team]['TotalLosses'] 
                    , all_seasons_dict[season][home_team]['HomeWins'] 
                    , all_seasons_dict[season][home_team]['HomeLosses'] 
                )
                away_bayesian_prob = get_home_bayesain_prob(
                    all_seasons_dict[season][away_team]['TotalWins'] 
                    , all_seasons_dict[season][away_team]['TotalLosses'] 
                    , all_seasons_dict[season][away_team]['AwayWins'] 
                    , all_seasons_dict[season][away_team]['AwayLosses'] 
                )

                # Get all of the data for the datframe before we update the season numbers
                data_arr = [season, date_format, home_team, away_team
                            , all_seasons_dict[season][home_team]['TotalWins'] #HomeTeamTotalWins
                            , all_seasons_dict[season][home_team]['TotalLosses'] #HomeTeamTotalLosses
                            , all_seasons_dict[season][away_team]['TotalWins'] #'AwayTeamTotalWins'
                            , all_seasons_dict[season][away_team]['TotalLosses'] #'AwayTeamTotalLosses'
                            , all_seasons_dict[season][home_team]['HomeWins'] #'HomeTeamHomeWins'
                            , all_seasons_dict[season][home_team]['HomeLosses'] #'HomeTeamHomeLosses'
                            , all_seasons_dict[season][away_team]['AwayWins'] #'AwayTeamAwayWins'
                            , all_seasons_dict[season][away_team]['AwayLosses'] #'AwayTeamAwayLosses'
                            , home_bayesian_prob #'HomeTeamBayesianWinningProb'
                            , away_bayesian_prob #'AwayTeamBayesianWinningProb'
                            , 0 if (home_bayesian_prob + away_bayesian_prob) == 0 else (home_bayesian_prob) / (home_bayesian_prob + away_bayesian_prob) #'HomeWinningProb'
                            , 0 if (home_bayesian_prob + away_bayesian_prob) == 0 else (away_bayesian_prob) / (home_bayesian_prob + away_bayesian_prob) #'AwayWinningProb'
                            , away_team if int(away_score) > int(home_score) else home_team #'WinningTeam'
                            ]
                game_df = pd.DataFrame([data_arr], columns = all_seasons_df.columns)

                if int(away_score) > int(home_score): #If the away team wins
                    #winning_team = away_team
                    all_seasons_dict[season][away_team]['TotalGameOutcomes'].append('W-A')
                    all_seasons_dict[season][away_team]['AwayGameOutcomes'].append('W')
                    all_seasons_dict[season][away_team]['TotalWins'] += 1
                    all_seasons_dict[season][away_team]['AwayWins'] += 1


                    #losing_team = home_team 
                    all_seasons_dict[season][home_team]['TotalGameOutcomes'].append('L-H')
                    all_seasons_dict[season][home_team]['HomeGameOutcomes'].append('L')
                    all_seasons_dict[season][home_team]['TotalLosses'] += 1
                    all_seasons_dict[season][home_team]['HomeLosses'] += 1


                else: #If the home team wins
                    #winning_team = home_team
                    all_seasons_dict[season][home_team]['TotalGameOutcomes'].append('W-H')
                    all_seasons_dict[season][home_team]['HomeGameOutcomes'].append('W')
                    all_seasons_dict[season][home_team]['TotalWins'] += 1
                    all_seasons_dict[season][home_team]['HomeWins'] += 1            

                    #losing_team = away_team
                    all_seasons_dict[season][away_team]['TotalGameOutcomes'].append('L-A')
                    all_seasons_dict[season][away_team]['AwayGameOutcomes'].append('L')
                    all_seasons_dict[season][away_team]['TotalLosses'] += 1
                    all_seasons_dict[season][away_team]['AwayLosses'] += 1 

                all_seasons_df = all_seasons_df.append(game_df)

                print('\t Away Team: {} - {}\n'.format(away_team, away_score))
                print('\t Home Team: {} - {}\n'.format(home_team, home_score))

    
    all_seasons_df['CorrectPrediction'] = all_seasons_df.apply(correct_prediction, axis = 1)
                
    return all_seasons_dict, all_seasons_df
