import os
import glob
import logging
import pickle
import pandas as pd
from sklearn.linear_model import LinearRegression

from tune.searches import searches

logger = logging.getLogger(__name__)

def save_configuration_result(search_name, data, clear=False):
    """Saves the provided data to the disk using the provided start_time as .csv"""
    if not os.path.exists('output'): os.makedirs('output')

    fn = 'output/search_%s.csv' % search_name
    if clear and os.path.isfile(fn): os.remove(fn)

    with open(fn,'a') as fd:
        fd.write(';'.join(map(str, data)) + '\n')

def print_results(search_name):
    df = pd.read_csv('output/search_%s.csv' % search_name, index_col=None, header=0)
    optimal = df.iloc[df['trueskill_mu'].idxmax()]
    logger.info(u'Optimal hyperparameters: N = %d, Cp = %.4f' % (optimal.N, optimal.Cp))

def save_plots(search_name, search):
    df = pd.read_csv('output/search_%s.csv' % search_name, index_col=None, header=0)

    for i, plot in enumerate(search['plots']):
        ax = df.plot(x=plot['xcol'], y=plot['ycol'], kind='scatter', figsize=(8,5))
        ax.set_xlabel(plot['xlabel'])
        ax.set_ylabel(plot['ylabel'])

        # Calculate linear regression
        if plot['linear-regression'] == True:
            X = df[plot['xcol']].values.reshape(-1, 1)
            y = df[plot['ycol']].values.reshape(-1, 1)
            lr = LinearRegression().fit(X, y)
            y_pred = lr.predict(X)
            ax.plot(X, y_pred, color='orange')

        fn = 'output/search_%s_%d.png' % (search_name, i)
        ax.get_figure().savefig(fn)
        logger.info('Saved %s' % fn)

def has_already_completed(args):
    if not args.overwrite:
        if os.path.isfile('output/search_' + args.search + '.csv'):
            completed_num_configs = sum(1 for line in open('output/search_%s.csv' % args.search)) - 1
            remaining_num_configs = args.num_configs - completed_num_configs

            if remaining_num_configs <= 0:
                logger.info('Hyperparameter search was already completed, call with --overwrite to re-run.')
                print_results(args.search)
                save_plots(args.search, searches[args.search])
                return True

            else:
                logger.info('Resuming from previous hyperparameter search.')
    
    return False
