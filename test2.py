from pystockfish import *
from GetMovesAndScores import GetMovesAndScores as GMAS
import ChessAI as AI
import chess

def splitStockBestMove(str):
    tmpstr = str.__repr__()

    index = tmpstr.find('move')
    if tmpstr[index+13] == 'q':
        sub = tmpstr[index + 8:index + 13]
        print("promotion!")
        print(sub)
    else:
        sub = tmpstr[index+8:index+12]

    return sub

def main():

    doTheGame()


def doTheGame():
    ai = AI.ChessAI()
    f = open("C:\\Users\\multimedia\\Desktop\\Py_ChessGame_0526\\test.txt", 'a')
    #gmas = GMAS()       #DeepPurple 객체 생성
    #while(board.is_game_over()):
    deep = Engine(depth=20)     #stockfish 객체생성
    chessBoard =  chess.Board()     #체스판생성

    chessPieceList = []     #stockfish에 넣을 체스말 리스트
    i = 0



    while True:
        #moves = gmas.get_bestMove(chessBoard)
        move = ai.ask(chessBoard)
        # print(moves)
        #move = moves[0]
        #print("DP선택된 move : ", move)
        try:
            chessBoard.push_uci(move)        #stockfish 체스명령어 푸시
        except ValueError:
            move+='Q'
            move = chess.Move.from_uci(move)
            chessBoard.push(move)

        i += 1
        chessPieceList.append(move)
        print(chessBoard)
        print("몇수:",i)


        deep.setposition(chessPieceList)
        tmp = deep.bestmove()
        ai.monte.tree.gmas.makeScores(chessBoard)
        tmp = splitStockBestMove(tmp)
        print("STOCK선택된 move : ", tmp)

        try:
            ai.refresh(tmp)
            chessBoard.push_uci(tmp)        #stockfish 체스명령어 푸시
        except ValueError:
            tmp+='q'
            ai.refresh(tmp)
            move = chess.Move.from_uci(tmp)
            chessBoard.push(move)
        chessPieceList.append(tmp)
        i += 1
        print("몇수:", i)
        print(chessBoard)

        if chessBoard.is_game_over():
            tmp=chessBoard.result()
            data = "대국 결과"
            data = data + tmp +" "+ "총 대국수:"+str(i)+"\n"
            f.write(data)

            f.close()
            break



            # probe_wdl(board)
            # Probes for win/draw/loss-information.
            # Returns 1 if the side to move is winning, 0 if it is a draw, and -1 if the side to move is losing.

if __name__ == '__main__':
    main()