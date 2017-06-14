import chess
from Board2Array import Board2Array as B2A

b2a=B2A()
b =chess.Board('r5k1/pq1b1rb1/3p1np1/1p1Ppp1p/1p5P/3PB1PN/P1Q1PPB1/1R3RK1 w - - 2 19')
print(b)
input = b2a.board2array(b)
print("------------------")
print(input)