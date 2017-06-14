import chess
import random
import MakeLegalMoves as MLM
class Model():
    def __init__(self, board):
        self.board = board.copy()
        self.moves = self.make_legalMoves()
        self.len = self.len_moves()
        self.scores = [0] * self.len
        self.randScores()
        self.sum = self.sum_scores()
        self.normalize_scores()


    def make_legalMoves(self):
        legal_moves = self.board.legal_moves
        mlm = MLM.MovesMaker()
        moves = mlm.make(legal_moves.__str__())
        return moves

    def len_moves(self):
        return len(self.moves)

    def randScores(self):
        for i in range(self.len):
            score = random.randint(1,101)
            self.scores[i] = score

    def view_scores(self):
        print(self.scores)

    def sum_scores(self):
        sum = 0
        for i in range(self.len):
            sum += self.scores[i]
        return sum

    def normalize_scores(self):
        for i in range(self.len):
            if self.sum != 0:
                self.scores[i] /= self.sum

    def get(self):
        return self.scores, self.moves

# b = chess.Board()
#
# model = Model(b)
#
# print(model.get())
