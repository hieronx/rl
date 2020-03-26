import logging, glob
import pandas as pd

logger = logging.getLogger(__name__)

def generate_custom_plots(args):
    size_vs_cp()
    trueskill_confidence()

def size_vs_cp():
    logger.info('Generating size vs Cp plot...')
    
    list = []
    for fn in glob.glob('output/final/search_cp-range-*.csv'):
        logger.info('Loading %s' % fn)
        list.append(pd.read_csv(fn, index_col=None, header=0, delimiter=';'))

    df = pd.concat(list, axis=0, ignore_index=True)
    best_Cp = df.groupby('size')
    best_Cp = df.iloc[best_Cp['trueskill_mu'].idxmax()]
    print(best_Cp.head())

    ax = best_Cp.boxplot(by='size', column=['Cp'], grid = False) 
    ax.set_xlabel('Board size')
    ax.set_ylabel('Cp')

    fn = 'output/size-vs-Cp.png'
    ax.get_figure().savefig(fn)
    logger.info('Saved %s' % fn)
    print()

def trueskill_confidence():
    logger.info('Generating TrueSkill confidence plot...')

    list = []
    for fn in glob.glob('output/final/search_cp-range-*.csv'):
        logger.info('Loading %s' % fn)
        list.append(pd.read_csv(fn, index_col=None, header=0, delimiter=';'))

    df = pd.concat(list, axis=0, ignore_index=True)

    ax = df.boxplot(by='size', column=['trueskill'], grid = False) 
    ax.set_xlabel('Board size')
    ax.set_ylabel('Trueskill σ-value')

    fn = 'output/trueskill-confidence.png'
    ax.get_figure().savefig(fn)
    logger.info('Saved %s' % fn)
