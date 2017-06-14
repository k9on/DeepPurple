import chess.pgn
from FenConvert import FenConvert as FC
'''
사용법 :

import ForFenMake_LoadData as LD

rd = LD.pgn_reader('./test.pgn')

rd.fenMake() # fen.txt에 fen 기보 생성됨

'''

def read_games(f): # pgn파일을 불러와 한 게임 별로 배열로 만들어 리턴함
    gs = []
    i=0
    print("\nPgn 배열로 변환!")
    while True:
        try:
            g = chess.pgn.read_game(f)
            gs.append(g) # 현재 포인터가 가르키는 게임을 리턴하고 다음 게임으로 포인터 이동
            if i%100 ==0 :
                print("\r",i,' ', end='', flush=True)
            i = i+1
        except KeyboardInterrupt:
            raise
        except:
            continue

        if not g: # 현재 포인터가 비어 있으면 yield 중지
            break
    gs.pop()
    return gs # yield 는 한방에 return 하지 않고 배열로 하나하나 추가 해놓고 다 끝나면 통째로 리턴

class pgn_reader:
    def __init__(self,filename=None):
        self.gs = []
        self.len = 0
        self.filename = filename
        self.load_games()
        self.count = 0
        self.fc = FC()

        #init을 수행하면
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
        result=g.headers['Result']
        return gns, result

    def fenMake(self, last=False):
        #
        #처음 부분에 사용된 파일인지 검사한후  사용 되었으면 return하여
        #다음 파일의 내용을 변환한다.
        #
        #fen기보를 생성
        print("\n게임변환")

        flag = False
        usedFile = open ('UsedFile.txt','a')
        # opengameFile = open('openGameFen.txt','a')
        # midGameFile = open('midGameFen.txt', 'a')
        # endGameFile = open('endGameFen.txt', 'a')
        # reducedOpenGameFile = open('reducedOpenGameFile.txt', 'a')
        allFen = open('AI35allFen.txt','a')
        whiteFen = open('AI35whiteFen.txt','a')

        usedFile.write(self.filename+"\n")

        with open('count.txt','r') as countFile:
            self.count = loadedCount = int(countFile.readline())

        for i in range(self.len):#입력된 pgn파일의 길이만큼 돈다
            if i % 100 == 0:
                print("\r",i, ' ', end='', flush=True)
            gns, result = self.get_game(self.gs[i])  # i번째 게임을
            gns.reverse()

            for j in range(len(gns) - 1):  # 처음부터 끝까지 입력과 출력으로 받음.
                if (i+1)*(j+1)+loadedCount > 20000000: #기보가 3천만개가 되면 종료
                    flag =True
                    break

                b = gns[j][1].board()
                # print(b)
                move = gns[j+1][1].move #리버스를 했으므로 보드 인덱스에서 +1 해야 다음 move
                # print(move)
                move_str = move.__str__()

                # if 0<=j and j<30:
                #     opengameFile.write(b.fen()+":"+move_str+":"+result+"\n")
                #     if i%15 ==0:
                #         reducedOpenGameFile.write(b.fen() + ":" + move_str + ":" + result + "\n")
                #         whiteFen.write(self.fc.turnFen(b.fen()) + ":" + self.fc.turnMove(b.fen(), move_str) + ":" + self.fc.turnResult( b.fen(), result) + "\n")
                #         self.count += 1
                # if 30<=j and j<60:
                #     midGameFile.write(b.fen()+":"+move_str+":"+result+"\n")
                #     reducedOpenGameFile.write(b.fen()+":"+move_str+":"+result+"\n")
                #     whiteFen.write(self.fc.turnFen(b.fen()) + ":" + self.fc.turnMove(b.fen(), move_str) + ":" + self.fc.turnResult(b.fen(), result) + "\n")
                #     self.count += 1
                # if 60<=j :
                #     endGameFile.write(b.fen()+":"+move_str+":"+result+"\n")
                #     reducedOpenGameFile.write(b.fen() + ":" + move_str + ":" + result + "\n")
                #     whiteFen.write(self.fc.turnFen(b.fen()) + ":" + self.fc.turnMove(b.fen(), move_str) + ":" + self.fc.turnResult(b.fen(), result) + "\n")
                #     self.count += 1
                allFen.write(b.fen() + ":" +move_str+":"+result+"\n")
                whiteFen.write(self.fc.turnFen(b.fen()) + ":" + self.fc.turnMove(b.fen(), move_str) + ":" + self.fc.turnResult(b.fen(), result) + "\n")
                self.count +=1

            if flag:
                break

        if self.count<30000000:
            print("\n변환된 기보 개수 : ",self.count,"\n--------------------")
            with open('count.txt', 'w') as countFile:
                countFile.write(str(self.count))

        # opengameFile.close()
        # midGameFile.close()
        # endGameFile.close()
        countFile.close()
        usedFile.close()
        allFen.close()
        whiteFen.close()
        # reducedOpenGameFile.close()



