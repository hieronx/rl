import os
import glob
import logging

logger = logging.getLogger(__name__)

def save_configuration_result(data, clear=False):
    """Saves the provided data to the disk using the provided start_time as .csv"""
    if not os.path.exists('output'): os.makedirs('output')

    fn = 'output/hyperparameter-search.csv'
    if clear and os.path.isfile(fn): os.remove(fn)

    with open(fn,'a') as fd:
        fd.write(','.join(map(str, data)) + '\n')