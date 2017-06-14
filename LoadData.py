import chess.pgn
import numpy as np
import random
import Board2Array as BA
from OneHotEncoding import OneHotEncode as OHE
import copy
import sys
'''
사용법 :

 # 폴더경로를 이용해 rd객체 하나를 생성
rd = pgn_reader('./test/test.pgn')

# get_data()메소드를 이용하면, index 몇번쨰 수인지, input 보드상태, output 명령어, r 승패결과
#index는 명령어가 몇번째 둔 수인지 나타내는 숫자. 홀수면 백, 짝수면 흑.
index, input, output, r = rd.get_data()


'''

def read_games(f): # pgn파일을 불러와 한 게임 별로 배열로 만들어 리턴함
    gs = []
    i=0
    print("\nPgn 배열로 변환!")
    while True:
        try:
            g = chess.pgn.read_game(f)
            gs.append(g) # 현재 포인터가 가르키는 게임을 리턴하고 다음 게임으로 포인터 이동
            if i%10 ==0 :
                print(i,' ', end='', flush=True)
            i = i+1
        except KeyboardInterrupt:
            raise
        except:
            continue

        if not g: # 현재 포인터가 비어 있으면 yield 중지
            break
    gs.pop()
    #print("Num of Games in The file : ",len(gs))
    return gs # yield 는 한방에 return 하지 않고 배열로 하나하나 추가 해놓고 다 끝나면 통째로 리턴

def startCnnResultAddIutput(input, startPosition):
    #처음cnn의 결과(시작점)을 iutput에 추가해 10번째 특징값을 만든다
    #startPosition은 시작점으로 64개의 1차원 배열로 되어 있다.

    addedFeature = []
    #result = copy.deepcopy(input)  # 8x8x9배열인 input값을 깊은복사


    for m in range(len(input)):
        result = copy.deepcopy(input[m])
        num = 0
        for i in range(8):
            for k in range(8):
               result[i][k].append(int(startPosition[m][num]))
               num += 1
        addedFeature.append(result)

    return addedFeature # 출발점이 포함된 8x8x10 input이 생성
def singleStartCnnResultAddIutput(input, startPosition):
    #처음cnn의 결과(시작점)을 iutput에 추가해 10번째 특징값을 만든다
    #startPosition은 시작점으로 64개의 1차원 배열로 되어 있다.

    #result = copy.deepcopy(input)  # 8x8x9배열인 input값을 깊은복사
    result = copy.deepcopy(input)
    num =0
    for i in range(8):
        for k in range(8):
            result[0][i][k].append(int(startPosition[num]))
            num += 1
    return result # 출발점이 포함된 8x8x10 input이 생성
class pgn_reader:
    def __init__(self,filename=None):
        self.gs = []
        self.len = 0
        self.filename = filename
        self.load_games()
        #init을 수행하면
    def __del__(self):
        print("소멸자 작동!")

    def set_pgn(self,filename):
        self.filename = filename

    def load_games(self):
        f = open(self.filename)
        self.gs = read_games(f)
        self.len = len(self.gs)

    def print_games(self):
        for i in range(self.len):
            self.info_game(i)
    def info_game(self, n):
        if(n >= self.len):
            return
        print(self.gs[n].headers)

    def get_game(self, g):
        gns = []
        result = ""
        gn = g.end()
        move_num = 0
        headers = g.headers
        while gn:
            gns.append((move_num, gn, gn.board().turn))

            move_num += 1
            gn = gn.parent
        #
        # for i in range(len(gns)):
        #     print(gns[i][1].board())
        #     print(gns[i-1][1].move)
        result=g.headers['Result']
        return gns, result

    def analyze(self, last = False):
        index=[]
        input=[]
        output=[]
        results = []
        ba = BA.Board2Array()
        print("\nAnalyze 작동")
        for i in range(self.len):
            if i%10 ==0 :
                print(i,' ', end='', flush=True)

            gns, result = self.get_game(self.gs[i])
            # print(result)
            flag = 1
            if last:
                flag = 0

            try:
                rand = random.randint(1, len(gns) - 1)
            except IndexError:
                continue
            b = gns[rand][1].board()
            b = ba.board2array(b)
            b = ba.addIndexFeature(b, len(gns) - rand)
            board = b  # b2array(b, flip)

            move = gns[rand - 1][1].move
            input.append(board)
            move_str = move.__str__()
            # print(move_str)
            output.append(move_str)
            results.append(result)
            index.append(len(gns) - rand)

        return index, input, output, results


    def allGameData(self,last = False):
        index = []
        resultInput = []
        resultOutput = []
        results = []
        ba = BA.Board2Array()
        print("\n게임변환")
        for i in range(self.len):
            if i % 10 == 0:
                print(i, ' ', end='', flush=True)
            gns, result = self.get_game(self.gs[i]) # i번째 게임을
            results.append(result)

            input1 = []
            output = []
            for j in range(len(gns)-2): #처음부터 끝까지 입력과 출력으로 받음.
                b = gns[len(gns) -(j+1)-2][1].board()
                b = ba.board2array(b)
                b = ba.addIndexFeature(b,len(gns) -(j+1)-2)
                board = b

                move = gns[len(gns)-j-2][1].move
                input1.append(board)

                move_str = move.__str__()
                output.append(move_str)

            resultInput.append(input1)
            resultOutput.append(output)

        return resultInput, resultOutput, results

    def allGameData2(self,last = False):
        index = []
        resultInput = []
        resultOutput = []
        results = []
        ba = BA.Board2Array()
        print("\n게임변환")
        for i in range(self.len):
            if i % 10 == 0:
                print(i, ' ', end='', flush=True)
            gns, result = self.get_game(self.gs[i]) # i번째 게임을
            for j in range(len(gns)-2): #처음부터 끝까지 입력과 출력으로 받음.
                b = gns[len(gns) -(j+1)-2][1].board()
                b = ba.board2array2(b)
                # b = ba.board2array(b)
                # b = ba.addIndexFeature(b,len(gns) -(j+1)-2)
                board = b
                results.append(result)
                move = gns[len(gns)-j-2][1].move
                resultInput.append(board)

                move_str = move.__str__()
                resultOutput.append(move_str)

        return resultInput, resultOutput, results


    def get_allGameData(self,last = False):
        input, output, result = self.allGameData(last)
        temp = self.trans2( input, output, result)
        return temp

    def get_allGameData2(self,last = False):
        input, output, result = self.allGameData2(last)
        input = np.reshape(input,[-1,8,8,15])
        temp = self.trans3( input, output, result)
        return temp

    def get_data(self, last = False):
        index, input, output, results = self.analyze(last)
        temp = self.trans(index, input, output, results)
        return temp


    def trans(self,index,input,output,results):
        rm = {'1-0': 1, '0-1': -1, '1/2-1/2': 0,'*':0}  # 게임의 끝, ( 백승 = 1, 흑승 = -1, 무승부, 0 )
        result= []
        boards = []
        for i in results:
            result.append(rm[i])

        # output을 grid로 변환

        output = self.outputToGrid(output)
        return index, input, output, result

    #모든 데이터를 얻을때 사용
    def trans2(self,input,output,results):
        rm = {'1-0': 1, '0-1': -1, '1/2-1/2': 0,'*':0}  # 게임의 끝, ( 백승 = 1, 흑승 = -1, 무승부, 0 )
        result= []
        for k in results:
            result.append(rm[k])
        tmpOutput =[]
        # output을 grid로 변환
        for i in range(len(input)):
            tmpOutput.append(self.outputToGrid(output[i]))

        return  input, tmpOutput , result

    #모든 데이터를 얻을때 사용
    def trans3(self,input,output,results):
        rm = {'1-0': [1,0,0,0], '0-1': [0,1,0,0], '1/2-1/2': [0,0,1,0],'*':[0,0,0,1]}  # 게임의 끝, ( 백승 = 1, 흑승 = -1, 무승부, 0 )
        result= []
        for k in results:
            result.append(rm[k])
        tmpOutput =[]
        # output을 grid로 변환
        for i in range(len(input)):
            tmpOutput.append(self.outputToGrid2(output[i]))

        return  input, tmpOutput , result

    def outputToGrid(self,move):
        #출발점과 도착점으로 이루어진 move를 격자 모양으로 만드는것
        output=[]
        uciOutput=[]
        ohe = OHE() #OHE객체 생성
        for i in range(len(move)):
            uciOutput.append(ohe.uciMoveToOnehot(move[i])) #4096 onehot

        output.append(uciOutput)

        return uciOutput

    def outputToGrid2(self,move):
        # 출발점과 도착점으로 이루어진 move를 격자 모양으로 만드는것
        tmp = 0;
        row = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        colomn = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7}
        x1 = row[move[0]]
        y1 = colomn[move[1]]
        x2 = row[move[2]]
        y2 = colomn[move[3]]
        tmp = (((x1 * 8) + y1) * 64) + ((x2 * 8) + y2)
        movearray = [0.0] * 4096
        movearray[tmp] = 1.0
        return movearray


