import numpy as np

from hex_skeleton import HexBoard

# sanity check that wins are detected
for i in range(0,2):
  winner = HexBoard.RED if i == 0 else HexBoard.BLUE
  looser = HexBoard.BLUE if i == 0 else HexBoard.RED
  board = HexBoard(3)
  
  board.place((1,1), looser)
  board.place((2,1), looser)
  board.place((1,2), looser)
  board.place((2,2), looser)
  board.place((0,0), winner)
  board.place((1,0), winner)
  board.place((2,0), winner)
  board.place((0,1), winner)
  board.place((0,2), winner)

  assert(board.check_win(winner) == True)
  assert(board.check_win(looser) == False)

  board.print()

# sanity check that random play will at some point end the game
endable_board = HexBoard(4)

while not endable_board.game_over:
  endable_board.place((np.random.randint(0, 4), np.random.randint(0, 4)), HexBoard.RED)

assert(endable_board.game_over == True)
assert(endable_board.check_win(HexBoard.RED) == True)
assert(endable_board.check_win(HexBoard.BLUE) == False)

print("Randomly filled board")
endable_board.print()