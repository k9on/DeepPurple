from GetMovesAndScores import GetMovesAndScores as GMAS
import tensorflow as tf
import numpy as np
import chess

b = chess.Board()

gvs = GMAS()

scores = gvs.makeScores(b)

print(scores)