from search.minimax import Minimax
from evaluate.dijkstra import Dijkstra

tune_configs = {
    'sanity-check': {
        'baseline': Minimax(1, None, Dijkstra(), False, False),
        'size': 3,
        'N': { 'min': 100, 'max': 10000 },
        'Cp': { 'min': 1.4, 'max': 1.4 }
    },
    'cp-range': {
        'baseline': Minimax(3, None, Dijkstra(), False, False),
        'size': 3,
        'N': { 'min': 5000, 'max': 5000 },
        'Cp': { 'min': 0.5, 'max': 2.0 }
    }
}