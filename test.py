from GetMovesAndScores import GetMovesAndScores as GMAS
from GetValueScores import GetValueScores as GVS
import numpy as np
# import chess
#
# gmas = GMAS()
#
# b = chess.Board()
# while True:
#     print(b.turn)
#     print(b)
#     moves = gmas.makeMoves(b)
#
#     scores = gmas.makeScores(b)
#
#     print(moves)
#
#     print(scores)
#
#     #str = input("input : ")
#     move = chess.Move.from_uci(moves[1][0])
#     b.push(move)

py = []
py.append(5)
py.append(4)
py.append(9)
py.append(1)
py.append(13)
arr = np.array(py)

test = (-arr).argsort()
print(arr[test[4]])