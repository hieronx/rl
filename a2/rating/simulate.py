from trueskill import Rating, rate_1vs1

from util.hexboard import HexBoard

def simulate_single_game(board_size, r1, r2, m1, m2, r1_first, r1_color, r2_color):
    board = HexBoard(board_size)
    r1_first = True if not r1_first else False
    r1_turn = True if r1_first else False

    first_color = r1_color if r1_first else r2_color
    second_color =  r2_color if r1_first else r1_color
    
    while not board.game_over():
        move = (m1 if r1_turn else m2).get_next_move(board, r1_color if r1_turn else r2_color)
        board.board[move] = r1_color if r1_turn else r2_color
        r1_turn = False if r1_turn else True

    if board.check_draw():
        r1, r2 = rate_1vs1(r1, r2, drawn=True)
    elif board.check_win(r1_color):
        r1, r2 = rate_1vs1(r1, r2, drawn=False)
    elif board.check_win(r2_color):
        r2, r1 = rate_1vs1(r2, r1, drawn=False)
    
    return r1, r2, r1_first