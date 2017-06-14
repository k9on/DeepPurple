from GetMovesAndScores import GetMovesAndScores as GMAS
import tensorflow as tf
import chess

b = chess.Board()
#b.push_san("b4")
pn = GMAS()

print(pn.makeMoves(b))

# while not b.is_game_over():
#     print(b)
#     if not b.turn :
#         print(pn.makeScores(b))
#         flag = True
#         while flag:
#             moves = b.legal_moves.__str__()
#             print("Legal moves : ", end="")
#             print(moves[37:-1])
#             choice = input("choice:")
#             if choice != "0":
#                 tmpBoard = b.copy()
#                 try:
#                     tmpBoard.push_san(choice)
#                     flag = False
#                 except ValueError:
#                     print("다시 선택해주세요")
#             else:
#                 flag = False
#         b.push_san(choice)
#     else:
#         print(pn.makeScores(b))
#         scores, moves = pn.makeMoves(b)  # 체스 보드를 넣는다.
#         print(moves)
#         print(scores)
#         move = chess.Move.from_uci(moves[0])
#         try:
#             print(move, moves[1],moves[2])
#         except:
#             try:
#                 print(move, moves[1])
#             except:
#                 print(move)
#         b.push(move)
#
#

