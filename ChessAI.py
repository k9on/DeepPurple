import Montecarlo as Monte


class ChessAI :
    def __init__(self):
        self.monte = Monte.Monte()
        self.decision = None


    def set(self,Board):
        self.monte.set_state(Board)

    def ask(self,Board):
        if self.monte.first :
            self.set(Board)
            self.monte.first = False
        self.analyze()
        self.refresh(self.decision)
        return self.decision

    def refresh(self,move):
        self.monte.inherit(move)

    def analyze(self):
        self.decision = self.monte.predict()

