configs = {
    'test': {
        'board_size': 4,
        'game_count': 1,
        'players': [
            { 'depth': None, 'time_limit': 0.5, 'search': 'minimax', 'eval': 'Dijkstra', 'rave_k': -1  },
            { 'depth': None, 'time_limit': 0.5, 'search': 'minimax', 'eval': 'Dijkstra', 'rave_k': -1  },
        ]
    },
    'random-vs-dijkstra': {
        'board_size': 4,
        'game_count': 200,
        'players': [
            { 'depth': 3, 'time_limit': None, 'search': 'minimax', 'eval': 'random', 'rave_k': -1  },
            { 'depth': 3, 'time_limit': None, 'search': 'minimax', 'eval': 'Dijkstra', 'rave_k': -1  },
            { 'depth': 4, 'time_limit': None, 'search': 'minimax', 'eval': 'Dijkstra', 'rave_k': -1  }
        ]
    },
    'depth-vs-time-limit': {
        'board_size': 4,
        'game_count': 200,
        'players': [
            { 'depth': 3, 'time_limit': None, 'search': 'minimax', 'eval': 'Dijkstra', 'rave_k': -1  },
            { 'depth': None, 'time_limit': 0.1, 'search': 'minimax', 'eval': 'Dijkstra', 'rave_k': -1  },
            { 'depth': None, 'time_limit': 1.0, 'search': 'minimax', 'eval': 'Dijkstra', 'rave_k': -1  },
        ]
    },
    'minimax-vs-mcts': {
        'board_size': 5,
        'game_count': 100,
        'players': [
            { 'depth': None, 'time_limit': 0.3, 'search': 'minimax', 'eval': 'Dijkstra', 'rave_k': -1  },
            { 'depth': None, 'time_limit': 0.3, 'search': 'mcts', 'eval': 'Dijkstra', 'rave_k': -1  },
        ]
    },
    'uct-vs-rave': {
        'board_size': 6,
        'game_count': 50,
        'players': [
            { 'depth': 500, 'time_limit': None, 'search': 'mcts', 'eval': 'Dijkstra', 'rave_k': -1 },
            { 'depth': 500, 'time_limit': None, 'search': 'mcts', 'eval': 'Dijkstra', 'rave_k': 250 },
        ]
    },
    'dijkstra-performance': {
        'board_size': 3,
        'game_count': 200,
        'players': [
            { 'depth': 3, 'time_limit': None, 'search': 'minimax', 'eval': 'random', 'rave_k': -1  },
            { 'depth': 3, 'time_limit': None, 'search': 'minimax', 'eval': 'Dijkstra', 'rave_k': -1  }
        ]
    }
}