import logging

from util.hexboard import HexBoard

logger = logging.getLogger(__name__)

player_names = ['']

def log_tree(node, level=0):
    output = []
    output.append((level, str(node.reward) + '/' + str(node.num_visits) + ' | ' + str(node.amaf_reward) + '/' + str(node.num_amaf_visits) + ' ' + str(node.board) + ' turn=' + HexBoard.PLAYER_ID_TO_NAME[node.turn]))

    for child in node.children:
        output = output + log_tree(child, level + 1)

    if level == 0:
        fn = 'output/mcts-debug.txt'
        with open(fn, 'w+', encoding='utf8') as output_file:
            for log in output:
                if log[0] is None:
                    output_file.write('\n')
                else:
                    out = ('\t' * log[0]) + log[1] + '\n'
                    output_file.write(out)
        
        logger.info('Saved %s' % fn)

    return output