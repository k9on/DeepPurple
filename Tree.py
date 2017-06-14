import Node
import Board_Stack as BS
import random as rand
from GetMovesAndScores import GetMovesAndScores as GMAS

import chess

import MakeLegalMoves as MLM

class Tree:

    def __init__(self): # 체스보드의 현재 상태를 입력받아 board_stack에 전달
        self.root_Node = None
        self.currentNode = None#현재 가리키는 노드를 임시로 저장
        self.board_stack = None #MCTS에서 각노드의 명령어를 사용할 Board_Stack
        self.gmas = GMAS()

    def reset_board(self,Board):
        self.board_stack = BS.Board_Stack(Board)
        self.set_RootNode()

    def inherit_tree(self, move):
        child = self.root_Node.find_move(move)
        self.board_stack.stack_push(move)
        try :
            child.del_parent()
            self.root_Node = child
            self.currentNode = self.root_Node
            print("상속완료")
        except :
            self.reset_board(self.board_stack.get_ChessBoard())
            print("상속 실패")
    def set_RootNode(self):
        self.root_Node = Node.Node(None,None) # 루트 노드 생성
        self.currentNode = self.root_Node #루트노드가 생성될 때 currentNode로 설정
        self.currentNode.set_Color(self.board_stack.get_Color())

    def go_root(self):
        self.currentNode = self.root_Node
        self.board_stack.clear_Stack()

    def set_BoardString(self,boardString):
        self.boardString = boardString

    def get_CurrentNode(self):#현재 tree가 가리키고 있는 노드 반환
        return self.currentNode

    #Board_Stack에 추가할 command를 갱신해야 함
    def set_CurrentNode(self ,node):#들어온 node를 currentNode로
        self.currentNode = node

        #입력받은 node의 명령어로 board_stack을 갱신
        self.board_stack.stack_push(node.get_Command())

    def add_ChildNode(self,node): #tree에서 currentNode에 자식 추가
        self.currentNode.add_ChildNode(node)

    # policy
    def make_policyNextChildren(self):
        tmpBoard = self.board_stack.get_ChessBoard()
        turn = tmpBoard.turn
        # 정책망에게 보드상태를 넘겨주면 가능한 moves를 넘겨 받는다.
        ######################## Random Policy #####################
        # model = rp.Model(tmpBoard)
        # policy_points, moves = model.get()
        policy_points, moves = self.gmas.makeMoves(tmpBoard)
        ############################################################
        children = []
        lenth = len(moves)
        if lenth == 0:
            print("자식 생성 오류, 정책망 추천 자식 없음")
        for i in range(lenth):
            move = chess.Move.from_uci(moves[i])
            tmpBoard.push(move)
            valueList = self.gmas.makeScores(tmpBoard)

            if turn:
                value = valueList[0] + valueList[2] * 0.05
            else :
                value = valueList[1] + valueList[2] * 0.05

            child = Node.Node(self.currentNode, moves[i], policy_points[i],value)
            child.set_Color(not turn)
            children.append(child)
            tmpBoard.pop()

        self.currentNode.set_Child(children)
        self.currentNode.on_Flag()


    # rollout
    def make_policyNextRandomChildBoard(self, board):
        tmpBoard = board.copy()
        turn = tmpBoard.turn
        #########################################
        # model = rp.Model(tmpBoard)
        # policy_points, moves = model.get()
        policy_points, moves =self.gmas.makeMoves(tmpBoard)

        #########################################
        children = []
        #print(tmpBoard)
        tmpNode = Node.Node(parent=None, command=None)
        lenth = len(moves)
        for i in range(lenth):
            tmpBoard2 = tmpBoard.copy()
            move = chess.Move.from_uci(moves[i])
            tmpBoard2.push(move)
            if tmpBoard2.is_game_over():

                if turn:
                    if tmpBoard2.result() == "1-0":
                        policy_points[i] = 1000000
                        #print("백이 이기는 수")
                    elif tmpBoard2.result() == "1/2-1/2":
                        if self.check_board(tmpBoard2):
                            policy_points[i] = 0
                        #print("백 : 비김")
                        #print(tmpBoard2)
                else:
                    if tmpBoard2.result() == "0-1":
                        #print("흑이 이기는 수")
                        policy_points[i] = 1000000
                    elif tmpBoard2.result() == "1/2-1/2":
                        if self.check_board(tmpBoard2):
                            policy_points[i] = 0
                        #print("흑 : 비김")
                        #print(tmpBoard2)

            child = Node.Node(tmpNode, moves[i], policy_points[i])
            child.set_Color(not turn)
            children.append(child)

        tmpNode.set_Child(children)
        distribution = tmpNode.get_policyDistribution()
        #tmpNode.print_childInfo()
        #print(distribution)
        flag = 0
        index = 0
        rand_num = rand.random()
        for i in distribution:
            if flag <= rand_num < flag+i:
                break
            else:
                index += 1
                flag += i
        try :
            childcommand = tmpNode.child[index].command
            move = chess.Move.from_uci(childcommand)
        except IndexError:
            mlm = MLM.MovesMaker()
            legalmoves = tmpBoard.legal_moves.__str__()
            moves = mlm.make(legalmoves)
            childcommand = rand.choice(moves)
            move = tmpBoard.push_san(childcommand)
            return tmpBoard
        #print(childcommand)

        tmpBoard.push(move)
        return tmpBoard

    def get_RootNode(self):
        return self.root_Node

    def get_GameOver(self):
        return self.board_stack.get_GameOver() #게임종료를 True False로 반환

    def get_Result(self):
        result = self.board_stack.get_Result()
        #print(self.board_stack.get_ChessBoard())
        if result == '*' :
            valueList = self.gmas.makeScores(self.get_currentBoard())

            max1 = max(valueList)
            if valueList[0] == max1 :
                result = "1-0"
            elif max1 == valueList[1] :
                result = "0-1"
            else :
                result = "1/2-1/2"
        return result

    def go_next(self):
        self.currentNode = self.currentNode.get_bestChild()
        self.currentNode.add_Visit(1)
        self.board_stack.stack_push(self.currentNode.command)

    def go_parrent(self):
        self.currentNode = self.currentNode.get_Parent()
        self.board_stack.stack_pop()

    def get_currentBoard(self):
        return self.board_stack.get_ChessBoard()

    def check_board(self,board):
        flag = False
        if board.can_claim_threefold_repetition():
            flag = True

        if board.can_claim_fifty_moves():
            flag = True
        if board.can_claim_draw():
            flag = True

        if board.is_fivefold_repetition():
            flag = True

        if board.is_seventyfive_moves():
            flag = True
        return flag