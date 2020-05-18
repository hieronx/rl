configs = {
    'not_working':[
        { 'id': 'AlphaZero 50 it. (1st attempt)', 'search': 'alphazero', 'time_limit': 0.1, 'model_path': 'alphazero/tests/old_50iterations_1.pt'},
        { 'id': 'AlphaZero w/ random weights', 'search': 'alphazero', 'time_limit': 0.1, 'model_path': 'alphazero/tests/random.pt'},
    ],
    'still_not_working':[
        { 'id': 'AlphaZero 50 it. (2nd attempt)', 'search': 'alphazero', 'time_limit': 0.1, 'model_path': 'alphazero/tests/old_50iterations_bugfixed.pt'},
        { 'id': 'AlphaZero 50 it. (1st attempt)', 'search': 'alphazero', 'time_limit': 0.1, 'model_path': 'alphazero/tests/old_50iterations_1.pt'},
        { 'id': 'AlphaZero w/ random weights', 'search': 'alphazero', 'time_limit': 0.1, 'model_path': 'alphazero/tests/random.pt'},
    ],
    'finally_success':[
        { 'id': 'AlphaZero 50 it. (1st success)', 'search': 'alphazero', 'time_limit': 0.1, 'model_path': 'alphazero/tests/new_50x50it_cp2_da1.1_q150.pt'},
        { 'id': 'AlphaZero 50 it. (2nd attempt)', 'search': 'alphazero', 'time_limit': 0.1, 'model_path': 'alphazero/tests/old_50iterations_bugfixed.pt'},
        { 'id': 'AlphaZero 50 it. (1st attempt)', 'search': 'alphazero', 'time_limit': 0.1, 'model_path': 'alphazero/tests/old_50iterations_1.pt'},
        { 'id': 'AlphaZero w/ random weights', 'search': 'alphazero', 'time_limit': 0.1, 'model_path': 'alphazero/tests/random.pt'},
    ],
    '50_50_mcts_minimax': [
        { 'id': 'AlphaZero 50 it. (1)', 'search': 'alphazero', 'time_limit': 0.1, 'model_path': 'alphazero/tests/new_50x50it_cp2_da1.1_q150.pt'},
        { 'id': 'AlphaZero 50 it. (2)', 'search': 'alphazero', 'time_limit': 0.1, 'model_path': 'alphazero/tests/new_50x50it_cp2_da1.1_q150_2.pt'},
        { 'id': 'ID-TT alpha-beta', 'search': 'minimax', 'depth': None, 'time_limit': 0.1, 'eval': 'Dijkstra', 'rave_k': -1 },
        { 'id': 'MCTS', 'search': 'mcts', 'depth': None, 'time_limit': 0.1, 'eval': 'Dijkstra', 'rave_k': -1 },
    ],
    '50_50_1000_mcts_minimax': [
        { 'id': 'AlphaZero 50 it. (1)', 'search': 'alphazero', 'time_limit': 0.1, 'model_path': 'alphazero/tests/new_50x50it_cp2_da1.1_q150.pt'},
        { 'id': 'AlphaZero 50 it. (2)', 'search': 'alphazero', 'time_limit': 0.1, 'model_path': 'alphazero/tests/new_50x50it_cp2_da1.1_q150_2.pt'},
        { 'id': 'AlphaZero 500 it.', 'search': 'alphazero', 'time_limit': 0.1, 'model_path': 'alphazero/tests/new_519x50it_cp2_da1.1_q150.pt'},
        { 'id': 'ID-TT alpha-beta', 'search': 'minimax', 'depth': None, 'time_limit': 0.1, 'eval': 'Dijkstra', 'rave_k': -1 },
        { 'id': 'MCTS', 'search': 'mcts', 'depth': None, 'time_limit': 0.1, 'eval': 'Dijkstra', 'rave_k': -1 },
    ],
    'training_length': [
        { 'id': '0 it. (random weights)', 'search': 'alphazero', 'time_limit': 0.1, 'model_path': 'alphazero/tests/random.pt'},
        { 'id': '50 it.', 'search': 'alphazero', 'time_limit': 0.1, 'model_path': 'alphazero/tests/new_50x50it_cp2_da1.1_q150.pt'},
        { 'id': '150 it.', 'search': 'alphazero', 'time_limit': 0.1, 'model_path': 'alphazero/tests/new_150x50it_cp2_da1.1_q150.pt'},
        { 'id': '500 it.', 'search': 'alphazero', 'time_limit': 0.1, 'model_path': 'alphazero/tests/new_519x50it_cp2_da1.1_q150.pt'}
    ],
    'cp': [
        { 'id': 'Cp: 0.4', 'search': 'alphazero', 'time_limit': 0.1, 'model_path': 'alphazero/tests/new_50x50it_cp0.4_da1.1_q150.pt'},
        { 'id': 'Cp: 2', 'search': 'alphazero', 'time_limit': 0.1, 'model_path': 'alphazero/tests/new_50x50it_cp2_da1.1_q150.pt'},
        { 'id': 'Cp: 5', 'search': 'alphazero', 'time_limit': 0.1, 'model_path': 'alphazero/tests/new_50x50it_cp5_da1.1_q150.pt'},
    ],
    'replay_buffer': [
        { 'id': 'Replay buffer size: 15', 'search': 'alphazero', 'time_limit': 0.1, 'model_path': 'alphazero/tests/new_50x50it_cp2_da1.1_q15.pt'},
        { 'id': 'Replay buffer size: 150', 'search': 'alphazero', 'time_limit': 0.1, 'model_path': 'alphazero/tests/new_50x50it_cp2_da1.1_q150.pt'},
        { 'id': 'Replay buffer size: 1500', 'search': 'alphazero', 'time_limit': 0.1, 'model_path': 'alphazero/tests/new_50x50it_cp2_da1.1_q1500.pt'},
    ],
    'temperature': [
        { 'id': 'Temperature: 1.0', 'search': 'alphazero', 'time_limit': 0.1, 'model_path': 'alphazero/tests/new_50x50it_cp2_da1.1_q1500.pt'},
        { 'id': 'Temperature: 1.0 => 0.2', 'search': 'alphazero', 'time_limit': 0.1, 'model_path': 'alphazero/tests/new_50x50it_cp2_da1.1_q1500_temp0.2.pt'},
    ],
    'dirichlet_alpha': [
        { 'id': 'Dirichlet alpha: 0.5', 'search': 'alphazero', 'time_limit': 0.1, 'model_path': 'alphazero/tests/new_50x50it_cp2_da0.5_q150.pt'},
        { 'id': 'Dirichlet alpha: 1.1', 'search': 'alphazero', 'time_limit': 0.1, 'model_path': 'alphazero/tests/new_50x50it_cp2_da1.1_q150.pt'},
        { 'id': 'Dirichlet alpha: 2.2', 'search': 'alphazero', 'time_limit': 0.1, 'model_path': 'alphazero/tests/new_50x50it_cp2_da2.2_q150.pt'},
    ]
    
}
