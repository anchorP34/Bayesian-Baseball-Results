# Bayesian-Baseball-Results
Predicting MLB Games Using Bayesian Models

# Head to Head Files
Each of the files that have Head To Head in them are the head to head matchups for each season. Each of these files can be recreated by referencing the head_to_head.py file like this:

final_results_dict_2018, final_results_df_2018 =  head_to_head([2018], None, None)

final_results_df_2018.to_excel('2018 Head to Head.xlsx', index = False)

# Bayesian Modeling with Machine Learning
Jupyter Notebook that runs analysis on machine learning algorithms compared to the accuracy of a regular Bayesian model.

# head_to_head.py
   Description: 
        Pulling every inning of every game from the input season from https://www.baseball-reference.com
    
    INPUT: 
        Season (int) - The season of the MLB year you would like to pull
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
