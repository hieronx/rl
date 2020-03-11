__Selection__: From root (R) to leaf (L). Leaf is any gamestate with no simulation and that is not terminal. 

__Expansion__: unless L ends the game decisively, create child nodes of L and choose node C from one of them. (randomly?) 
Child nodes are any valid moves from the game position defined by L.

__Simulation__: complete one random playout from node C. Return the reward from the perspective of the search player.

__Backpropagation__: use the result of the playout to update information in the nodes on the path from C to R.
