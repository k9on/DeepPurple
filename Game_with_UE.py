# encoding : UTF-8
from socket import *
import threading
import chess
import ChessAI as AI
import MakeLegalMoves as MLM
import time
from pystockfish import *

 # CMD Protocol

# index area
min_index = 0
max_index = 6363

#select model
single_mode = 7001
dual_mode = 7002
train_mode = 7003

# select turn
White_turn = 7201
Black_turn = 7202


# make new board
new_board = 7400

# check_move
ack = 7500
nack = 7600

# get start index
start_index = 77

# legal moves for one
legals = 78

# result game
White_win  = 8001
Black_win = 8002
Draw = 8003

# wait for Input
waiting = 9999

# restart game
restart = 9901

# undo
undo = 9900

def splitStockBestMove(str):
    tmpstr = str.__repr__()

    index = tmpstr.find('move')
    if tmpstr[index+13] == 'q' or tmpstr[index+13] == 'b' or tmpstr[index+13] == 'r' or tmpstr[index+13] == 'n':
        sub = tmpstr[index + 8:index + 13]
        print("promotion!")
        print(sub)
    else:
        sub = tmpstr[index+8:index+12]

    return sub



class network:
    def __init__(self):
        self.client = socket(AF_INET, SOCK_STREAM)
        self.th = threading.Thread(target=self.recv, args=())
        self.client.connect(("127.0.0.1", 30005))
        self.board = chess.Board()
        self.ai = AI.ChessAI()
        self.player_turn = White_turn
        self.mode = single_mode
        self.mlm = MLM.MovesMaker()
        self.stockAI = Engine(depth=20)     #stockfish 객체생성
        self.list = []
        self.ai_turn = False
    def set_board(self,str):
        self.board = chess.Board(str)
        self.list = []

    def new_board(self):
        print("new board")
        self.board = chess.Board()
        if self.mode == single_mode and self.player_turn == Black_turn :
            self.ask_AI()
        elif self.mode == train_mode :
            self.ask_AI()


    def recv(self):
        while True:
            print("ready")
            #self.send(str(waiting))
            try:
                data = self.client.recv(1024)
            except ConnectionAbortedError:
                self.client.close()
                self.reconnect()
                data = self.client.recv(1024)
            data = data.decode('utf-8')
            if not data:
                print("restart")
                break
            print("receive",data)
            self.transCommand(data)


        self.restart()

    def send(self,tmp):
        tmp = str(tmp)
        print(tmp)
        zero_num = 4 - len(tmp)
        for i in range(zero_num):
            tmp = "0" + tmp
        tmp = tmp.encode(encoding='UTF-8')

        try:
            self.client.send(tmp)
        except (ConnectionAbortedError, OSError):
            self.client.close()
            self.reconnect()
            self.client.send(tmp)

    def transCommand(self,str):
        cmd = int(str)
        if cmd >=min_index and cmd <= max_index:
            self.cmd2uci(cmd)
        else :
            self.cmd2other(cmd)

    def cmd2other(self,cmd):
        first = cmd // 100
        last = cmd  % 100

        if first == start_index:
            if self.mode != train_mode:
                self.getNext(cmd)

        elif cmd == single_mode:
            self.mode = single_mode
        elif cmd == dual_mode:
            self.mode = dual_mode
        elif cmd == train_mode:
            self.mode = train_mode

        elif cmd == White_turn :
            self.player_turn = White_turn
            self.step = 2
        elif cmd == Black_turn :
            self.player_turn = Black_turn
            self.step = 2

        elif cmd == new_board :
            self.new_board()
        elif cmd == undo :
            self.undo()
        elif cmd == restart :
            self.new_board()

    def cmd2uci(self,cmd):
        row = {0:"1",1:"2",2:"3",3:"4",4:"5",5:"6",6:"7",7:"8"}
        col= {0:"a",1:"b",2:"c",3:"d",4:"e",5:"f",6:"g",7:"h"}
        first = cmd // 100
        # print(first)
        last = cmd%100
        # print(last)

        one = first % 8
        # print(one)
        two = first // 8
        # print(two)
        thr = last % 8
        # print(thr)
        four = last // 8
        # print(four)

        one = col[one]
        two = row[two]
        thr = col[thr]
        four = row[four]

        uci = one + two + thr + four
        # print(uci)
        # check if Legal
        # sekf,check_legal(uci)

        try:
            try :
                self.board.push_uci(uci)
                self.list.append(uci)
            except:
                uci += "q"
                self.board.push_uci(uci)
                self.list.append(uci)
                print("promotion!!")
            self.list.append(uci)
            print(self.board)
            if cmd == 406:
                self.send("0705")
            elif cmd == 402:
                self.send("0003")
            elif cmd == 6062:
                self.send("6361")
            elif cmd == 6058:
                self.send("5659")

            if self.board.is_game_over():
                time.sleep(1)
                if self.board.result() == '1-0':
                    self.send(8001)
                elif self.board.result() == '0-1':
                    self.send(8002)
                elif self.board.result() == '1/2-1/2':
                    self.send(8003)

            if self.ai.monte.tree.root_Node != None:
                self.ai.refresh(uci.__str__())
            #self.send(ack)
            if self.mode == single_mode:
                self.ask_AI()
        except:
            print("가능한 수가 아닙니다.")




    def uci2cmd(self,cmd):
        row = {"1": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5, "7": 6, "8": 7}
        col = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

        cmd1 = 100 * (row[cmd[1]] * 8 + col[cmd[0]]) + row[cmd[3]] * 8 + col[cmd[2]]

        if cmd1 < 1000:
            cmd = cmd1.__repr__()
            cmd = '0' + cmd
            if cmd1 < 100 :
                cmd = '0' + cmd
            if cmd1 < 10:
                cmd = '0' + cmd
        else:

            cmd = cmd1.__repr__()
        return cmd

    #def check_legal(self, uci):

    def run(self):
        self.th.start()

    def end(self):
        self.th.join()
        self.client.close()

    def ask_AI(self):
        if (not self.board.turn) :
            choice = self.ai.ask(self.board)
            self.list.append(choice)
            self.board.push_uci(choice)
        else :
            self.stockAI.setposition(self.list)
            tmp = self.stockAI.bestmove()
            choice = splitStockBestMove(tmp)
            try:
                self.board.push_uci(choice)
                if self.ai.monte.tree.root_Node :
                    self.ai.refresh(choice)
                self.list.append(choice)
            except ValueError:
                choice = choice + "q"
                move = chess.Move.from_uci(choice)
                self.board.push(move)
                self.ai.refresh(choice)
                self.list.append(choice)


        choice = self.uci2cmd(choice)
        self.send(str(choice))
        time.sleep(1)
        if str(choice) == "6062":
            self.send("6361")
        elif str(choice) == "6058":
            self.send("5659")
        elif str(choice) == "0406":
            self.send("0705")
        elif str(choice) == "0402":
            self.send("0003")
        print(self.board)

        if self.board.is_game_over():
            if self.board.result() == '1-0':
                self.send(8001)
            elif self.board.result() == '0-1':
                self.send(8002)
            elif self.board.result() == '1/2-1/2':
                self.send(8003)
        else :
            if self.mode == train_mode:
                self.ask_AI()

    def undo(self):
        self.board.pop()
        self.board.pop()

        # 현재 수를 기준으로 다음 수를 찾기

    def getNext(self, cmd):
        # board는 파이썬 현재 board 상태
        # chesspiece는

        tmpuci = []

        cmd1 = cmd % 100
        # print(last)
        cmd = cmd1.__repr__()
        if cmd1< 10:
            cmd = '0'+ cmd

        tmplegal = self.board.legal_moves
        tmplegal = tmplegal.__repr__()
        legalList = self.mlm.make(tmplegal)

        for i in range(len(legalList)):
            tmp = self.board.parse_san(legalList[i])
            tmp = tmp.__repr__()
            tmp = tmp[15:-2]

            tmpcmd = self.uci2cmd(tmp)

            if int(tmpcmd[0]) == int(cmd[0]) and int(tmpcmd[1]) == int(cmd[1]):
                tmpuci.append(int(tmpcmd[2]) * 10 + int(tmpcmd[3]))


        tmpstr = "78"
        for i in range(len(tmpuci)):
            flag = False
            if tmpuci[i] < 10 :
                flag = True
            tmpnum = tmpuci[i]
            repr_tmp = tmpnum.__repr__()
            if flag :
                repr_tmp = "0" + repr_tmp
            tmpret = tmpstr + repr_tmp
            self.send(tmpret)



    def reconnect(self):
        self.client = socket(AF_INET, SOCK_STREAM)

        try:
            self.client.connect(("127.0.0.1", 30005))
        except ConnectionRefusedError:
            pass

    def restart(self):
        net = network()
        net.send('7777')
        net.run()
        net.end()

def main():
    net = network()
    net.send('7777')
    net.run()
    net.end()


if __name__ == "__main__":
    main()