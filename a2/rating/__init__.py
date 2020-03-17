from search.minimax import Minimax
from search.mcts import MCTS

from evaluate.dijkstra import Dijkstra
from evaluate.astar import AStar
from evaluate.random import RandomEval

def get_search_class(player, disable_tt=False):
    if player['search'] == 'minimax':
        return Minimax(player['depth'], player['time_limit'], get_eval_class(player['eval']), False, disable_tt)
    elif player['search'] == 'mcts':
        return MCTS(player['depth'], player['time_limit'], 1.4, False, player['amaf_alpha'])

def get_eval_class(eval_method):
    if eval_method == 'Dijkstra':
        return Dijkstra()
    elif eval_method == 'AStar':
        return AStar()
    elif eval_method == 'random':
        return RandomEval()
