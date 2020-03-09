import os
import glob
import logging
import pickle

logger = logging.getLogger(__name__)

def save_configuration_result(data, clear=False):
    """Saves the provided data to the disk using the provided start_time as .csv"""
    if not os.path.exists('output'): os.makedirs('output')

    fn = 'output/hyperparameter-search.csv'
    if clear and os.path.isfile(fn): os.remove(fn)

    with open(fn,'a') as fd:
        fd.write(','.join(map(str, data)) + '\n')

def resume_previous_run(args, new_settings):
    continue_previous_run = False
    remaining_num_configs = args.num_configs
    if not args.overwrite:
        cached_settings = load_search_settings()
        if cached_settings is not None and cached_settings == new_settings:
            completed_num_configs = sum(1 for line in open('output/hyperparameter-search.csv')) - 1
            remaining_num_configs = args.num_configs - completed_num_configs

            if remaining_num_configs <= 0:
                logger.critical('Hyperparameter search was already completed, call with --overwrite to re-run.')
                exit()

            else:
                continue_previous_run = True
                logger.info('Resuming from previous hyperparameter search, for the remaining %d/%d configurations.' % (remaining_num_configs, args.num_configs))
    
    return continue_previous_run, remaining_num_configs


def save_search_settings(settings):
    if not os.path.exists('output'): os.makedirs('output')

    fn = 'output/hyperparameter-search.data'
    if os.path.isfile(fn): os.remove(fn)

    settings_file = open(fn, 'ab') 
    pickle.dump(settings, settings_file)                      
    settings_file.close()

    logger.info('Saved %s' % fn)

def load_search_settings():
    fn = 'output/hyperparameter-search.data'

    if not os.path.isfile(fn): return None

    settings_file = open(fn, 'rb')      
    settings = pickle.load(settings_file)
    settings_file.close()

    return settings