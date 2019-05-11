# Bayesian-Baseball-Results
Predicting MLB Games Using Bayesian Models

# Head to Head Files
Each of the files that have Head To Head in them are the head to head matchups for each season. Each of these files can be recreated by referencing the head_to_head.py file like this:

final_results_dict_2018, final_results_df_2018 =  head_to_head([2018], None, None)

final_results_df_2018.to_excel('2018 Head to Head.xlsx', index = False)
