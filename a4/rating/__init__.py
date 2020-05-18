from evaluate.astar import AStar
from evaluate.dijkstra import Dijkstra
from evaluate.random import RandomEval
from search.alphazero import AlphaZero
from search.mcts import MCTS
from search.minimax import Minimax


def get_search_class(player, disable_tt=False, board_size=5):
    if player['search'] == 'minimax':
        return Minimax(player['depth'], player['time_limit'], get_eval_class(player['eval']), False, disable_tt)
    elif player['search'] == 'mcts':
        return MCTS(player['depth'], player['time_limit'], 0.4, False, player['rave_k'])
    elif player['search'] == 'alphazero':
        return AlphaZero(player['model_path'], player['id'], board_size)

def get_eval_class(eval_method):
    if eval_method == 'Dijkstra':
        return Dijkstra()
    elif eval_method == 'AStar':
        return AStar()
    elif eval_method == 'random':
        return RandomEval()
