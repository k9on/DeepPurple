import TreeForMakeTree as TR
import chess
import pickle
class Monte:
    def __init__(self, repeat_num = 10000, select_depth = 1000, simulation_num = 1,expend_point = 5):
        self.tree = TR.Tree()  # 트리 생성
        self.expand_point = expend_point  # 확장 기준값
        self.select_depth = select_depth  # 선택을 종료할 깊이
        self.repeat_num = repeat_num  # 반복 수행할 횟수
        self.simulation_num = simulation_num

    def set_state(self,Board):
        self.tree.reset_board(Board)

    def make(self):
        for i in range(self.repeat_num):
            print("\r%d" % i , end="")
            self.search()
            if i % 10 == 0:
                try:
                    self.save()
                    print(self.choice())
                except:
                    print("저장 실패")

        # choice
        choice = self.choice()
        print("")
        return choice

    def search(self):
        depth = 0
        select_Flag = True

        while select_Flag:
        # selection
            # print(depth)
            result_selection = self.selection(depth)  # selection에서 게임이 끝이 났으면 0, 끝이 안났으면 1
            depth += 1
            if result_selection == 0  : # 0 gameover 1 more 2 simulation
                select_Flag = False

        result = self.tree.get_Result()

        # backpropagation
        self.backpropagation(result)

    def selection(self, depth):

        #print("selection")
        if self.tree.get_GameOver():  # 보드가 게임이 끝난 상태라면 ( 흰승 : 1, 검은승 : -1, 무: 0
            return 0

        else:  # 보드가 게임이 끝나지 않았다면
            if depth > 20:
                return 0
            if not self.tree.currentNode.get_Flag():  # 자식노드 체크
                    # 자식 노드 생성
                self.tree.make_policyNextChildren()
                # 다음 노드로
            self.tree.go_next()

            return 1



    def backpropagation(self, result):
        if self.tree.currentNode.is_root():
            return 0
        else:
            self.tree.currentNode.renew_result(result)
            self.tree.go_parrent()
            return self.backpropagation(result)

    def choice(self):
        root = self.tree.get_RootNode()
        index = root.For_root_choice()
        self.tree.currentNode.print_childInfo()
        return root.child[index].command


    def save(self):
        file = open('tree.txt', 'wb')
        pickle.dump(self.tree.get_RootNode(), file)
    def load(self):
        file = open('tree.txt', 'rb')
        s  = pickle.load(file)
        self.tree.set_RootNode(s)


class test:
     def __init__(self):
         self.a = 0

class test2:
      def __init__(self):
        self.a = test()

b = chess.Board()
monte = Monte()
monte.set_state(b)
#monte.load()

c = monte.make()
print(c)
