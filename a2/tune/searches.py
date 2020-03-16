from search.minimax import Minimax
from search.mcts import MCTS
from evaluate.dijkstra import Dijkstra

searches = {
    'sanity-check': {
        'baseline': MCTS(100, None, 1.4, False),
        'size': 4,
        'N': { 'min': 100, 'max': 10000 },
        'Cp': { 'min': 1.4, 'max': 1.4 },
        'num-configs': 50,
        'confidence-threshold': 0.1,
        'plots': [
            {
                'create': lambda df: df.plot(x='N', y='config_mu', kind='scatter', figsize=(8,5)),
                'xlabel': 'N',
                'ylabel': 'TrueSkill μ-value'
            }
        ]
    },
    'cp-range': {
        'baseline': Minimax(3, None, Dijkstra(), False, False),
        'size': 3,
        'N': { 'min': 5000, 'max': 5000 },
        'Cp': { 'min': 0.5, 'max': 2.0 },
        'num-configs': 100,
        'confidence-threshold': 1.0,
        'plots': [
            {
                'create': lambda df: df.plot(x='Cp', y='config_mu', kind='scatter', figsize=(8,5)),
                'xlabel': 'Cp',
                'ylabel': 'TrueSkill μ-value'
            }
        ]
    },
    'n-range': {
        'baseline': Minimax(3, None, Dijkstra(), False, False),
        'size': 3,
        'N': { 'min': 100, 'max': 10000 },
        'Cp': { 'min': 1.4, 'max': 1.4 },
        'num-configs': 100,
        'confidence-threshold': 1.0,
        'plots': [
            {
                'create': lambda df: df.plot(x='N', y='config_mu', kind='scatter', figsize=(8,5)),
                'xlabel': 'N',
                'ylabel': 'TrueSkill μ-value'
            }
        ]
    },
    'n-vs-cp': {
        'baseline': Minimax(3, None, Dijkstra(), False, False),
        'size': 3,
        'N': { 'min': 100, 'max': 10000 },
        'Cp': { 'min': 0.5, 'max': 2.0 },
        'num-configs': 250,
        'confidence-threshold': 1.0,
        'plots': [
            {
                'create': lambda df: df.plot(x='N', y='Cp', kind='scatter', figsize=(8,5)),
                'xlabel': 'N',
                'ylabel': 'Cp'
            }
        ]
    }
}