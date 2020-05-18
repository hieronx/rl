configs = {
    'test': [
        { 'id': 'minimax', 'search': 'minimax', 'depth': None, 'time_limit': 0.1, 'eval': 'Dijkstra', 'rave_k': -1 },
        { 'id': 'mcts', 'search': 'mcts', 'depth': None, 'time_limit': 0.1, 'eval': 'Dijkstra', 'rave_k': -1 },
    ],
    '50_50_mcts_minimax': [
        { 'id': 'AZ_50x50_1', 'search': 'alphazero', 'model_path': 'alphazero/tests/new_50x50it_cp2_da1.1_q150.pt'},
        { 'id': 'AZ_50x50_2', 'search': 'alphazero', 'model_path': 'alphazero/tests/new_50x50it_cp2_da1.1_q150_2.pt'},
        { 'id': 'minimax', 'search': 'minimax', 'depth': None, 'time_limit': 0.1, 'eval': 'Dijkstra', 'rave_k': -1 },
        { 'id': 'mcts', 'search': 'mcts', 'depth': None, 'time_limit': 0.1, 'eval': 'Dijkstra', 'rave_k': -1 },
    ]
}
