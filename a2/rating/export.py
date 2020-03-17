import os
import pandas as pd
import matplotlib.pyplot as plt
import glob
import logging

from . import get_search_class

logger = logging.getLogger(__name__)

def save_result(config_name, data, clear=False):
    """Saves the provided data to the disk using the provided start_time as .csv"""
    if not os.path.exists('output'): os.makedirs('output')

    fn = 'output/%s.csv' % config_name
    if clear and os.path.isfile(fn): os.remove(fn)

    with open(fn, 'a') as fd:
        fd.write(';'.join(map(str, data)) + '\n')

def save_plots(args, player_permutations):
    """Saves the plots that were generated from the player permutations to the disk using the timestamp as part of the filename"""
    df = pd.read_csv("output/" + args.config + ".csv", index_col=None, header=0, delimiter=';')
    if not os.path.exists('output'): os.makedirs('output')

    for i, (p1, p2) in enumerate(player_permutations):
        m1, m2 = get_search_class(p1, args.disable_tt), get_search_class(p2, args.disable_tt)

        games = df[(df['p1'] == str(m1)) & (df['p2'] == str(m2))] 
       
        ax = games.plot(x='game_id', y=['r1_mu', 'r2_mu'], figsize=(8,5), grid=True)
        
        ax.set_xlabel("Number of games")
        ax.set_ylabel("TrueSkill μ-value")
        
        ax.legend([str(m1), str(m2)])
        
        fn = 'output/%s_%s.png' % (args.config, i+1)
        ax.get_figure().savefig(fn)
        logger.info('Saved %s' % fn)