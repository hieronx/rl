configs = {
    'random-vs-dijkstra': {
        'board_size': 4,
        'game_count': 200,
        'players': [
            { 'depth': 3, 'time_limit': None, 'search': 'minimax', 'eval': 'random' },
            { 'depth': 3, 'time_limit': None, 'search': 'minimax', 'eval': 'Dijkstra' },
            { 'depth': 4, 'time_limit': None, 'search': 'minimax', 'eval': 'Dijkstra' }
        ]
    },
    'depth-vs-time-limit': {
        'board_size': 4,
        'game_count': 200,
        'players': [
            { 'depth': 3, 'time_limit': None, 'search': 'minimax', 'eval': 'Dijkstra' },
            { 'depth': None, 'time_limit': 0.1, 'search': 'minimax', 'eval': 'Dijkstra' },
            { 'depth': None, 'time_limit': 1.0, 'search': 'minimax', 'eval': 'Dijkstra' },
        ]
    },
    'minimax-vs-mcts': {
        'board_size': 3,
        'game_count': 100,
        'players': [
            { 'depth': None, 'time_limit': 0.1, 'search': 'minimax', 'eval': 'Dijkstra' },
            { 'depth': None, 'time_limit': 0.1, 'search': 'mcts', 'eval': None },
        ]
    },
    'dijkstra-performance': {
        'board_size': 3,
        'game_count': 200,
        'players': [
            { 'depth': 3, 'time_limit': None, 'search': 'minimax', 'eval': 'random' },
            { 'depth': 3, 'time_limit': None, 'search': 'minimax', 'eval': 'Dijkstra' }
        ]
    }
}