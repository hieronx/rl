import logging, glob
import pandas as pd

logger = logging.getLogger(__name__)

def generate_custom_plots(args):
    """Generates the custom plots"""
    # size_vs_cp()
    minimax_vs_mcts_by_time()
    # trueskill_confidence()

def size_vs_cp():
    """Runs the size vs cp test. In this test we see what CP is most useful on what board size."""
    logger.info('Generating size vs Cp plot...')
    
    combined_results = []
    for fn in glob.glob('output/final/search_cp-range-*.csv'):
        logger.info('Loading %s' % fn)
        combined_results.append(pd.read_csv(fn, index_col=None, header=0, delimiter=';'))

    df = pd.concat(combined_results, axis=0, ignore_index=True)
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

def minimax_vs_mcts_by_time():
    logger.info('Generating Minimax vs MCTS by time limit plot...')
    
    for board_size in [5, 6]:
        combined = pd.DataFrame(columns=['time_limit', 'player', 'trueskill_mu'])
        for time_limit in [0.1, 0.2, 0.3, 0.4, 0.5]:
            fn = 'output/final/minimax-vs-mcts-%d-%.1fs.csv' % (board_size, time_limit)
            logger.info('Loading %s' % fn)
            df = pd.read_csv(fn, index_col=None, header=0, delimiter=';')

            combined.loc[len(combined)] = [time_limit, 'Minimax', df.tail(1)['r1_mu'].values[0]]
            combined.loc[len(combined)] = [time_limit, 'MCTS', df.tail(1)['r2_mu'].values[0]]
        
        pivot = combined.pivot(index='time_limit', columns='player', values='trueskill_mu')
        ax = pivot.plot(kind='line', grid = False) 
        ax.set_xlabel('Time limit (s)')
        ax.set_ylabel('Trueskill mu-value')

        fn = 'output/minimax-vs-mcts-by-time_size-%d.png' % board_size
        ax.get_figure().savefig(fn)
        logger.info('Saved %s' % fn)


def trueskill_confidence():
    """Runs the trueskill confidence script which plots the confidence"""
    logger.info('Generating TrueSkill confidence plot...')

    combined_results = []
    for fn in glob.glob('output/final/search_cp-range-*.csv'):
        logger.info('Loading %s' % fn)
        combined_results.append(pd.read_csv(fn, index_col=None, header=0, delimiter=';'))

    df = pd.concat(combined_results, axis=0, ignore_index=True)

    ax = df.boxplot(by='size', column=['trueskill'], grid = False) 
    ax.set_xlabel('Board size')
    ax.set_ylabel('Trueskill σ-value')

    fn = 'output/trueskill-confidence.png'
    ax.get_figure().savefig(fn)
    logger.info('Saved %s' % fn)
