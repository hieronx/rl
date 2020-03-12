from trueskill import Rating, rate_1vs1

from util.hexboard import HexBoard

def simulate_single_game(board_size, r1, r2, m1, m2, r1_first, r1_color, r2_color):
    board = HexBoard(board_size)
    r1_first = True if not r1_first else False
    r1_turn = True if r1_first else False

    first_color = r1_color if r1_first else r2_color
    second_color =  r2_color if r1_first else r1_color
    
    winner = board.get_winner()
    while winner is None:
        move = (m1 if r1_turn else m2).get_next_move(board, r1_color if r1_turn else r2_color)
        board.place(move, r1_color if r1_turn else r2_color)
        r1_turn = False if r1_turn else True
        winner = board.get_winner()

    if winner == HexBoard.EMPTY:
        r1, r2 = rate_1vs1(r1, r2, drawn=True)
    elif winner == r1_color:
        r1, r2 = rate_1vs1(r1, r2, drawn=False)
    elif winner == r2_color:
        r2, r1 = rate_1vs1(r2, r1, drawn=False)
    
    return r1, r2, r1_first