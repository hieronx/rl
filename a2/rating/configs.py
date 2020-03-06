configs = {
    'random-vs-Dijkstra': {
        'board_size': 4,
        'game_count': 200,
        'players': [
            { 'depth': 3, 'time_limit': None, 'search': 'Minimax', 'eval': 'random' },
            { 'depth': 3, 'time_limit': None, 'search': 'Minimax', 'eval': 'Dijkstra' },
            { 'depth': 4, 'time_limit': None, 'search': 'Minimax', 'eval': 'Dijkstra' }
        ]
    },
    'depth-vs-time-limit': {
        'board_size': 4,
        'game_count': 200,
        'players': [
            { 'depth': 3, 'time_limit': None, 'search': 'Minimax', 'eval': 'Dijkstra' },
            { 'depth': None, 'time_limit': 0.1, 'search': 'Minimax', 'eval': 'Dijkstra' },
            { 'depth': None, 'time_limit': 1.0, 'search': 'Minimax', 'eval': 'Dijkstra' },
        ]
    },
    'Minimax-vs-MCTS': {
        'board_size': 3,
        'game_count': 100,
        'players': [
            { 'depth': None, 'time_limit': 0.1, 'search': 'Minimax', 'eval': 'Dijkstra' },
            { 'depth': None, 'time_limit': 0.1, 'search': 'MCTS', 'eval': 'Dijkstra' },
        ]
    },
    'Dijkstra-performance': {
        'board_size': 3,
        'game_count': 200,
        'players': [
            { 'depth': 3, 'time_limit': None, 'search': 'Minimax', 'eval': 'random' },
            { 'depth': 3, 'time_limit': None, 'search': 'Minimax', 'eval': 'Dijkstra' }
        ]
    }
}