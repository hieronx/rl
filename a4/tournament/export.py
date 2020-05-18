import os

import matplotlib.pyplot as plt
import pandas as pd


def save_results(tournament_name, line, clear=False):
    if not os.path.exists('output'): os.makedirs('output')

    fn = 'output/tournament_%s.csv' % tournament_name
    if clear and os.path.isfile(fn): os.remove(fn)

    with open(fn, 'a') as fd:
        fd.write(';'.join(map(str, line)) + '\n')

def save_plots(tournament_name):
    df = pd.read_csv("output/tournament_" + tournament_name + ".csv", index_col=None, header=0, delimiter=';')

    y_values = df.columns[:len(df.columns)//2] # Get first half, as the second half contains the sigma values
    player_ids = [player[:-3] for player in y_values] # Remove _mu postfix

    ax = df.plot(y=y_values, use_index=True, figsize=(8,5), grid=True)
    
    ax.set_xlabel("Number of games")
    ax.set_ylabel("TrueSkill μ-value")
    
    ax.legend(player_ids)
    
    fn = 'output/tournament_%s.png' % tournament_name
    ax.get_figure().savefig(fn)
