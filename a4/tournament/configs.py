configs = {
    'test': [
        { 'id': 'minimax', 'search': 'minimax', 'depth': None, 'time_limit': 0.1, 'eval': 'Dijkstra', 'rave_k': -1 },
        { 'id': 'mcts', 'search': 'mcts', 'depth': None, 'time_limit': 0.1, 'eval': 'Dijkstra', 'rave_k': -1 },
    ],
    'not_working':[
        { 'id': 'AZ_50it_50g_old', 'search': 'alphazero', 'model_path': 'alphazero/tests/old_50iterations_1.pt'},
        { 'id': 'Random', 'search': 'alphazero', 'model_path': 'alphazero/tests/random.pt'},
    ],
    'still_not_working':[
        { 'id': 'AZ_50it_50g_bugfixed', 'search': 'alphazero', 'model_path': 'alphazero/tests/old_50iterations_bugfixed.pt'},
        { 'id': 'AZ_50it_50g_old', 'search': 'alphazero', 'model_path': 'alphazero/tests/old_50iterations_1.pt'},
        { 'id': 'Random', 'search': 'alphazero', 'model_path': 'alphazero/tests/random.pt'},
    ],
    'finally_success':[
        { 'id': 'AZ_50it_50g_success', 'search': 'alphazero', 'model_path': 'alphazero/tests/new_50x50it_cp2_da1.1_q150.pt'},
        { 'id': 'AZ_50it_50g_bugfixed', 'search': 'alphazero', 'model_path': 'alphazero/tests/old_50iterations_bugfixed.pt'},
        { 'id': 'AZ_50it_50g_old', 'search': 'alphazero', 'model_path': 'alphazero/tests/old_50iterations_1.pt'},
        { 'id': 'Random', 'search': 'alphazero', 'model_path': 'alphazero/tests/random.pt'},
    ],
    '50_50_mcts_minimax': [
        { 'id': 'AZ_50it_50g_1', 'search': 'alphazero', 'model_path': 'alphazero/tests/new_50x50it_cp2_da1.1_q150.pt'},
        { 'id': 'AZ_50it_50g_2', 'search': 'alphazero', 'model_path': 'alphazero/tests/new_50x50it_cp2_da1.1_q150_2.pt'},
        { 'id': 'minimax', 'search': 'minimax', 'depth': None, 'time_limit': 0.1, 'eval': 'Dijkstra', 'rave_k': -1 },
        { 'id': 'mcts', 'search': 'mcts', 'depth': None, 'time_limit': 0.1, 'eval': 'Dijkstra', 'rave_k': -1 },
    ],
    '50_50_1000_mcts_minimax': [
        { 'id': 'AZ_50it_50g_1', 'search': 'alphazero', 'model_path': 'alphazero/tests/new_50x50it_cp2_da1.1_q150.pt'},
        { 'id': 'AZ_50it_50g_2', 'search': 'alphazero', 'model_path': 'alphazero/tests/new_50x50it_cp2_da1.1_q150_2.pt'},
        { 'id': 'AZ_1000it_50g', 'search': 'alphazero', 'model_path': 'alphazero/tests/new_519x50it_cp2_da1.1_q150.pt'},
        { 'id': 'minimax', 'search': 'minimax', 'depth': None, 'time_limit': 0.1, 'eval': 'Dijkstra', 'rave_k': -1 },
        { 'id': 'mcts', 'search': 'mcts', 'depth': None, 'time_limit': 0.1, 'eval': 'Dijkstra', 'rave_k': -1 },
    ],
    'training_length': [
        { 'id': 'AZ_0it', 'search': 'alphazero', 'model_path': 'alphazero/tests/random.pt'},
        { 'id': 'AZ_50it_50g', 'search': 'alphazero', 'model_path': 'alphazero/tests/new_50x50it_cp2_da1.1_q150.pt'},
        { 'id': 'AZ_150it_50g', 'search': 'alphazero', 'model_path': 'alphazero/tests/new_150x50it_cp2_da1.1_q150.pt'},
        { 'id': 'AZ_500it_50g', 'search': 'alphazero', 'model_path': 'alphazero/tests/new_519x50it_cp2_da1.1_q150.pt'},
        { 'id': 'AZ_1000it_50g', 'search': 'alphazero', 'model_path': 'alphazero/tests/new_1000x50it_cp2_da1.1_q150.pt'},
    ],
    'cp': [
        { 'id': 'AZ_50it_50g_cp0.4', 'search': 'alphazero', 'model_path': 'alphazero/tests/new_50x50it_cp0.4_da1.1_q150.pt'},
        { 'id': 'AZ_50it_50g_cp2', 'search': 'alphazero', 'model_path': 'alphazero/tests/new_50x50it_cp2_da1.1_q150.pt'},
        { 'id': 'AZ_50it_50g_cp5', 'search': 'alphazero', 'model_path': 'alphazero/tests/new_50x50it_cp5_da1.1_q150.pt'},
    ],
    'replay_buffer': [
        { 'id': 'AZ_50it_50g_rp15', 'search': 'alphazero', 'model_path': 'alphazero/tests/new_50x50it_cp2_da1.1_q15.pt'},
        { 'id': 'AZ_50it_50g_rp150', 'search': 'alphazero', 'model_path': 'alphazero/tests/new_50x50it_cp2_da1.1_q150.pt'},
        { 'id': 'AZ_50it_50g_rp1500', 'search': 'alphazero', 'model_path': 'alphazero/tests/new_50x50it_cp2_da1.1_q1500.pt'},
    ],
    'temperature': [
        { 'id': 'AZ_50it_50g_no_temp', 'search': 'alphazero', 'model_path': 'alphazero/tests/new_50x50it_cp2_da1.1_q1500.pt'},
        { 'id': 'AZ_50it_50g_temp0.2', 'search': 'alphazero', 'model_path': 'alphazero/tests/new_50x50it_cp2_da1.1_q1500_temp0.2.pt'},
    ],
    'dirichlet_alpha': [
        { 'id': 'AZ_50it_50g_da0.5', 'search': 'alphazero', 'model_path': 'alphazero/tests/new_50x50it_cp2_da0.5_q150.pt'},
        { 'id': 'AZ_50it_50g_da1.1', 'search': 'alphazero', 'model_path': 'alphazero/tests/new_50x50it_cp2_da1.1_q150.pt'},
        { 'id': 'AZ_50it_50g_da2.2', 'search': 'alphazero', 'model_path': 'alphazero/tests/new_50x50it_cp2_da2.2_q150.pt'},
    ]
    
}
