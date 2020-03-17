import os
import pandas as pd
import matplotlib.pyplot as plt
import glob
import logging

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
    df = pd.read_csv("output/" + args.config + ".csv", index_col=None, header=0)
    if not os.path.exists('output'): os.makedirs('output')

    for i, (p1, p2) in enumerate(player_permutations):
        games = df[(df['p1_search'] == p1['search']) & (df['p1_depth'].astype(str) == str(p1['depth'])) & (df['p1_eval'] == p1['eval']) & (df['p1_time_limit'].astype(str) == str(p1['time_limit']))
                & (df['p2_search'] == p2['search']) & (df['p2_depth'].astype(str) == str(p2['depth'])) & (df['p2_time_limit'].astype(str) == str(p2['time_limit'])) & (df['p2_eval'] == p2['eval'])] 
       
        ax = games.plot(x='game_id', y=['r1_mu', 'r2_mu'], figsize=(8,5), grid=True)
        
        ax.set_xlabel("Number of games")
        ax.set_ylabel("TrueSkill μ-value")
        
        p1_name = p1['search'] + ', ' + p1['eval'] + (" (depth " + str(p1['depth']) + ")" if p1['depth'] is not None else " (time limit " + str(p1['time_limit']) + "s)")
        p2_name = p2['search'] + ', ' + p2['eval'] + (" (depth " + str(p2['depth']) + ")" if p2['depth'] is not None else " (time limit " + str(p2['time_limit']) + "s)")
        ax.legend([p1_name, p2_name]);
        
        fn = 'output/%s_%s.png' % (args.config, i+1)
        ax.get_figure().savefig(fn)
        logger.info('Saved %s' % fn)