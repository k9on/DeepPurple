import Node
import Board_Stack as BS
import random as rand
from GetMovesAndScores import GetMovesAndScores as GMAS

import chess

promotion = {"a7a8","a7b8","b7a8","b7c8","c7b8","c7c8","c7d8",}

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

    def set_RootNode(self, root=None):
        if root :
            self.root_Node = root # 루트 노드 생성
        else :
            self.root_Node = Node.Node(None,None)
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
        poliy_sum = sum(policy_points)
        ############################################################
        children = []
        lenth = len(moves)
        for i in range(lenth):
            tmpBoard2 = tmpBoard.copy()
            move = chess.Move.from_uci(moves[i])
            tmpBoard2.push(move)
            if self.check_board(tmpBoard2):
                policy_points[i] = 0
            valueList = self.gmas.makeScores(tmpBoard2)
            if tmpBoard.turn :
                value = valueList[0]
            else :
                value = valueList[1]
            value += valueList[2] * 0.1
            if tmpBoard2.is_game_over() :
                if turn :
                    if tmpBoard2.result() == "1-0" :
                        policy_points[i] = 1000000

                    elif tmpBoard2.result() == "1/2-1/2":
                        if self.check_board(tmpBoard2):
                            policy_points[i] = 0

                else :
                    if tmpBoard2.result() == "0-1":
                        policy_points[i] = 1000000
                    elif tmpBoard2.result() == "1/2-1/2":
                        if self.check_board(tmpBoard2):
                            policy_points[i] = 0

            child = Node.Node(self.currentNode, moves[i], policy_points[i] / poliy_sum,value)
            child.set_Color(not turn)
            children.append(child)

        self.currentNode.set_Child(children)
        self.currentNode.on_Flag()

    def get_RootNode(self):
        return self.root_Node

    def get_GameOver(self):
        return self.board_stack.get_GameOver() #게임종료를 True False로 반환

    def get_Result(self):
        result = self.board_stack.get_Result()
        if result == '*' :
            valueList = self.gmas.makeScores(self.get_currentBoard())
            print(valueList)
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