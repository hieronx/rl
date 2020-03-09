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