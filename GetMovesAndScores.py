import chess
import numpy as np
import tensorflow as tf
import os

from Board2Array import Board2Array as B2A
from OneHotEncoding import OneHotEncode as OHE


class GetMovesAndScores:
    def __init__(self):
        #입력으로 체스 보드를 받아온다

        self.promotion = 0.5 # legalmoves중에서 몇 퍼센트까지 만들지 결정 비율
        self.penalty = 0.01 # Score계산에서
        self.madeMoves = [] # 선택된 Moves의 list
        self.madeMovesScores =[] # madeMoves의 점수들이 들어 있는 list
        self.flag = False
        self.sess = tf.Session()
        self.sess2 = tf.Session()

        PN_Name = "PN/"
        VN_Name = "VN/"
        # base_policy2

        with tf.variable_scope("PN"):
            self.X = tf.placeholder(tf.float32, [None, 8, 8, 35], name="X")  # 체스에서 8X8X10 이미지를 받기 위해 64
            self.K = tf.placeholder(tf.float32, [None], name="K")

            self.W1 = tf.get_variable("W1", shape=[5, 5, 35, 128], initializer=tf.contrib.layers.xavier_initializer())
            self.B1 = tf.get_variable("B1", initializer=tf.random_normal([128], stddev=0.01))
            self.L1 = tf.nn.relu(tf.nn.conv2d(self.X, self.W1, strides=[1, 1, 1, 1], padding='SAME') + self.B1)

            self.W2 = tf.get_variable("W2", shape=[3, 3, 128, 128], initializer=tf.contrib.layers.xavier_initializer())
            self.B2 = tf.get_variable("B2", initializer=tf.random_normal([128], stddev=0.01))
            self.L2 = tf.nn.relu(tf.nn.conv2d(self.L1, self.W2, strides=[1, 1, 1, 1], padding='SAME') + self.B2)

            self.W3 = tf.get_variable("W3", shape=[3, 3, 128, 128], initializer=tf.contrib.layers.xavier_initializer())
            self.B3 = tf.get_variable("B3", initializer=tf.random_normal([128], stddev=0.01))
            self.L3 = tf.nn.relu(tf.nn.conv2d(self.L2, self.W3, strides=[1, 1, 1, 1], padding='SAME') + self.B3)

            self.W4 = tf.get_variable("W4", shape=[3, 3, 128, 128], initializer=tf.contrib.layers.xavier_initializer())
            self.B4 = tf.get_variable("B4", initializer=tf.random_normal([128], stddev=0.01))
            self.L4 = tf.nn.relu(tf.nn.conv2d(self.L3, self.W4, strides=[1, 1, 1, 1], padding='SAME') + self.B4)

            self.W5 = tf.get_variable("W5", shape=[3, 3, 128, 128], initializer=tf.contrib.layers.xavier_initializer())
            self.B5 = tf.get_variable("B5", initializer=tf.random_normal([128], stddev=0.01))
            self.L5 = tf.nn.relu(tf.nn.conv2d(self.L4, self.W5, strides=[1, 1, 1, 1], padding='SAME') + self.B5)

            self.W6 = tf.get_variable("W6", shape=[3, 3, 128, 128], initializer=tf.contrib.layers.xavier_initializer())
            self.B6 = tf.get_variable("B6", initializer=tf.random_normal([128], stddev=0.01))
            self.L6 = tf.nn.relu(tf.nn.conv2d(self.L5, self.W6, strides=[1, 1, 1, 1], padding='SAME') + self.B6)

            self.W7 = tf.get_variable("W7", shape=[3, 3, 128, 128], initializer=tf.contrib.layers.xavier_initializer())
            self.B7 = tf.get_variable("B7", initializer=tf.random_normal([128], stddev=0.01))
            self.L7 = tf.nn.relu(tf.nn.conv2d(self.L6, self.W7, strides=[1, 1, 1, 1], padding='SAME') + self.B7)

            self.W8 = tf.get_variable("W8", shape=[3, 3, 128, 128], initializer=tf.contrib.layers.xavier_initializer())
            self.B8 = tf.get_variable("B8", initializer=tf.random_normal([128], stddev=0.01))
            self.L8 = tf.nn.relu(tf.nn.conv2d(self.L7, self.W8, strides=[1, 1, 1, 1], padding='SAME') + self.B8)

            self.W9 = tf.get_variable("W9", shape=[3, 3, 128, 128], initializer=tf.contrib.layers.xavier_initializer())
            self.B9 = tf.get_variable("B9", initializer=tf.random_normal([128], stddev=0.01))
            self.L9 = tf.nn.relu(tf.nn.conv2d(self.L8, self.W9, strides=[1, 1, 1, 1], padding='SAME') + self.B9)

            self.W10 = tf.get_variable("W10", shape=[3, 3, 128, 128],
                                       initializer=tf.contrib.layers.xavier_initializer())
            self.B10 = tf.get_variable("B10", initializer=tf.random_normal([128], stddev=0.01))
            self.L10 = tf.nn.relu(tf.nn.conv2d(self.L9, self.W10, strides=[1, 1, 1, 1], padding='SAME') + self.B10)

            self.W11 = tf.get_variable("W11", shape=[3, 3, 128, 128],
                                       initializer=tf.contrib.layers.xavier_initializer())
            self.B11 = tf.get_variable("B11", initializer=tf.random_normal([128], stddev=0.01))
            self.L11 = tf.nn.relu(tf.nn.conv2d(self.L10, self.W11, strides=[1, 1, 1, 1], padding='SAME') + self.B11)

            self.W12 = tf.get_variable("W12", shape=[3, 3, 128, 128],
                                       initializer=tf.contrib.layers.xavier_initializer())
            self.B12 = tf.get_variable("B12", initializer=tf.random_normal([128], stddev=0.01))
            self.L12 = tf.nn.relu(tf.nn.conv2d(self.L11, self.W12, strides=[1, 1, 1, 1], padding='SAME') + self.B12)

            self.W13 = tf.get_variable("W13", shape=[1, 1, 128, 128],
                                       initializer=tf.contrib.layers.xavier_initializer())
            self.B13 = tf.get_variable("B13", initializer=tf.random_normal([128], stddev=0.01))
            self.L13 = tf.nn.relu(tf.nn.conv2d(self.L12, self.W13, strides=[1, 1, 1, 1], padding='SAME') + self.B13)

            self.FlatLayer = tf.reshape(self.L13, [-1, 8 * 8 * 128])
            self.Flat_W = tf.get_variable("Flat_W", shape=[8 * 8 * 128, 4096],
                                          initializer=tf.contrib.layers.xavier_initializer())
            self.Flat_B = tf.get_variable("Flat_B", initializer=tf.random_normal([4096], stddev=0.01))

            self.hypothesis = tf.matmul(self.FlatLayer, self.Flat_W) + self.Flat_B

            self.SMhy = tf.nn.softmax(self.hypothesis)
            self.sotf = tf.nn.softmax(self.K)
            # tf.get_variable_scope().reuse_variables() # 변수를 재사용하기 위한 방법
            self.sess.run(tf.global_variables_initializer())

        self.PN_saves = {PN_Name + "W1": self.W1, PN_Name + "B1": self.B1,
                         PN_Name + "W2": self.W2, PN_Name + "B2": self.B2,
                         PN_Name + "W3": self.W3, PN_Name + "B3": self.B3,
                         PN_Name + "W4": self.W4, PN_Name + "B4": self.B4,
                         PN_Name + "W5": self.W5, PN_Name + "B5": self.B5,
                         PN_Name + "W6": self.W6, PN_Name + "B6": self.B6,
                         PN_Name + "W7": self.W7, PN_Name + "B7": self.B7,
                         PN_Name + "W8": self.W8, PN_Name + "B8": self.B8,
                         PN_Name + "W9": self.W9, PN_Name + "B9": self.B9,
                         PN_Name + "W10": self.W10, PN_Name + "B10": self.B10,
                         PN_Name + "W11": self.W11, PN_Name + "B11": self.B11,
                         PN_Name + "W12": self.W12, PN_Name + "B12": self.B12,
                         PN_Name + "W13": self.W13, PN_Name + "B13": self.B13,
                         PN_Name + "Flat_W": self.Flat_W, PN_Name + "Flat_B": self.Flat_B,
                         }

        saver = tf.train.Saver(self.PN_saves)
        ckpt = tf.train.get_checkpoint_state(os.path.dirname('./PNCheckpoint/'))
        # print(ckpt.model_checkpoint_path)
        if ckpt and ckpt.model_checkpoint_path:
            print("정책망 로딩 완료")
            saver.restore(self.sess, ckpt.model_checkpoint_path)
            # print("\n체크포인트 파일 재사용 = ", ckpt.model_checkpoint_path)


        with tf.variable_scope("VN", reuse=False):
            self.VX = tf.placeholder(tf.float32, [None, 8, 8, 31], name="X")  # 체스에서 8X8X10 이미지를 받기 위해 64

            self.VW1 = tf.get_variable("W1", shape=[5, 5, 31, 128], initializer=tf.contrib.layers.xavier_initializer())
            self.VB1 = tf.get_variable("B1", initializer=tf.random_normal([128], stddev=0.01))
            self.VL1 = tf.nn.relu(tf.nn.conv2d(self.VX, self.VW1, strides=[1, 1, 1, 1], padding='SAME') + self.VB1)

            self.VW2 = tf.get_variable("W2", shape=[3, 3, 128, 128], initializer=tf.contrib.layers.xavier_initializer())
            self.VB2 = tf.get_variable("B2", initializer=tf.random_normal([128], stddev=0.01))
            self.VL2 = tf.nn.relu(tf.nn.conv2d(self.VL1, self.VW2, strides=[1, 1, 1, 1], padding='SAME') + self.VB2)

            self.VW3 = tf.get_variable("W3", shape=[3, 3, 128, 64], initializer=tf.contrib.layers.xavier_initializer())
            self.VB3 = tf.get_variable("B3", initializer=tf.random_normal([64], stddev=0.01))
            self.VL3 = tf.nn.relu(tf.nn.conv2d(self.VL2, self.VW3, strides=[1, 1, 1, 1], padding='SAME') + self.VB3)

            self.VW4 = tf.get_variable("W4", shape=[3, 3, 64, 64], initializer=tf.contrib.layers.xavier_initializer())
            self.VB4 = tf.get_variable("B4", initializer=tf.random_normal([64], stddev=0.01))
            self.VL4 = tf.nn.relu(tf.nn.conv2d(self.VL3, self.VW4, strides=[1, 1, 1, 1], padding='SAME') + self.VB4)

            # self.VW5 = tf.get_variable("W5", shape=[3, 3, 64, 64], initializer=tf.contrib.layers.xavier_initializer())
            # self.VB5 = tf.get_variable("B5", initializer=tf.random_normal([64], stddev=0.01))
            # self.VL5 = tf.nn.relu(tf.nn.conv2d(self.VL4, self.VW5, strides=[1, 1, 1, 1], padding='SAME') + self.VB5)
            #
            # self.VW6 = tf.get_variable("W6", shape=[3, 3, 64, 64], initializer=tf.contrib.layers.xavier_initializer())
            # self.VB6 = tf.get_variable("B6", initializer=tf.random_normal([64], stddev=0.01))
            # self.VL6 = tf.nn.relu(tf.nn.conv2d(self.VL5, self.VW6, strides=[1, 1, 1, 1], padding='SAME') + self.VB6)

            self.VFlatLayer = tf.reshape(self.VL4, [-1, 8* 8 * 64])

            self.VFlat_W = tf.get_variable("Flat_W", shape=[4096, 3],
                                          initializer=tf.contrib.layers.xavier_initializer())
            self.VFlat_B = tf.get_variable("Flat_B", initializer=tf.random_normal([3], stddev=0.01))

            self.Vhypothesis = tf.matmul(self.VFlatLayer, self.VFlat_W) + self.VFlat_B

            self.VSMhy = tf.nn.softmax(self.Vhypothesis)

            #tf.get_variable_scope().reuse_variables()  # 변수를 재사용하기 위한 방법
            self.sess2.run(tf.global_variables_initializer())

        self.VN_saves = {VN_Name + "W1": self.VW1, VN_Name + "B1": self.VB1,
                         VN_Name + "W2": self.VW2, VN_Name + "B2": self.VB2,
                         VN_Name + "W3": self.VW3, VN_Name + "B3": self.VB3,
                         VN_Name + "W4": self.VW4, VN_Name + "B4": self.VB4,
                         # VN_Name + "W5": self.VW5, VN_Name + "B5": self.VB5,
                         # VN_Name + "W6": self.VW6, VN_Name + "B6": self.VB6,

                         VN_Name + "Flat_W": self.VFlat_W, VN_Name + "Flat_B": self.VFlat_B}




        saver = tf.train.Saver(self.VN_saves)
        ckpt2 = tf.train.get_checkpoint_state(os.path.dirname('./VNCheckpoint/'))
        if ckpt2 and ckpt2.model_checkpoint_path:
            #print(ckpt.model_checkpoint_path)
            saver.restore(self.sess2, ckpt2.model_checkpoint_path)
            #print("\n체크포인트 파일 재사용 = ", ckpt.model_checkpoint_path)


    def get_PN_Model(self,startCnnInput):
        getSoftmax = self.sess.run(self.SMhy, feed_dict = {self.X:startCnnInput})
        return getSoftmax

    def get_VN_Model(self,startCnnInput):

        getSoftmax = self.sess2.run(self.VSMhy, feed_dict = {self.VX:startCnnInput})
        return getSoftmax

    def make_PN_Input(self, chessBoard):
        startCnnInput = []
        startCnnInput.append(B2A().board2array(chessBoard))

        return startCnnInput

    def make_VN_Input(self, chessBoard):

        startCnnInput = []
        startCnnInput.append(B2A().board2array5(chessBoard))
        #startCnnInput = tf.to_float(startCnnInput)

        return startCnnInput

    def makeScores(self,chessBoard):
        startCnnInput= self.make_VN_Input(chessBoard)
        softMax = self.get_VN_Model(startCnnInput)
        softMax = np.array(softMax[0])

        return softMax

    def makeMoves(self, chessBoard):
        startCnnInput = self.make_PN_Input(chessBoard)
        softMax = self.get_PN_Model(startCnnInput)
        softMax = np.array(softMax[0])
        ArgMaxOfSoftmax = (-softMax).argsort()
        # 내림차순으로 분류한 것을 리스트로 반환 받는다
        # softMAxArgMax는 크기별로 Index만 저장 되어있다. 0~4095

        ohe = OHE()
        score = []
        moves = []
        i = 0
        child = 0
        # print(chessBoard)

        numOfLegalMoves = len(chessBoard.legal_moves)
        numOfChild = 5

        # 만드려고 하는 자식 개수보다 가능한 move 갯수가 적을때
        if numOfLegalMoves < numOfChild:
            numOfChild = numOfLegalMoves

        for j in range(4096):

            # print(i, "번째 선택된 softmax 값 = ", softMax[softMaxArgMax[i]])
            try:
                tmpMove = ohe.indexToMove4096(ArgMaxOfSoftmax[i])
                tmpMove2 = chess.Move.from_uci(tmpMove)
                tmpMove3 = chess.Move.from_uci(tmpMove+"q")

                    # tmpMove = chess.Move.from_uci(tmpMove) # 주석처리: 선피쉬랑 붙기 위해 String 자체를 사용
            except:
                print(i)
                print(numOfChild)
                print(numOfLegalMoves)

            if tmpMove2 in chessBoard.legal_moves:
                #print(i)
                # print(i+1,"번째 softmax값 에서 ",child+1, "번째 선택된 child 값 = ", softMax[softMaxArgMax[i]], "  move = ", tmpMove)
                score.append(softMax[ArgMaxOfSoftmax[i]])
                moves.append(tmpMove)  # tmpMove가 legal이면 추가
                child += 1
            else:
                if tmpMove3 in chessBoard.legal_moves:
                    # print(i)
                    # print(i+1,"번째 softmax값 에서 ",child+1, "번째 선택된 child 값 = ", softMax[softMaxArgMax[i]], "  move = ", tmpMove)
                    score.append(softMax[ArgMaxOfSoftmax[i]])
                    moves.append(tmpMove+"q")  # tmpMove가 legal이면 추가
                    child += 1

            if softMax[ArgMaxOfSoftmax[i]] <= 0.03 and child != 0:  # 만드려고 하는 자식 갯수보다 많으면 반환
                break
            i += 1

        return score, moves

    # def softmax(self,x):
    #     scoreMatExp = np.exp(np.asarray(x))
    #     return scoreMatExp / scoreMatExp.sum(0)

    def indexToMove2(self, index):
        row1 = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
        colomn1 = {0: '1', 1: '2', 2: '3', 3: '4', 4: '5', 5: '6', 6: '7', 7: '8'}

        a = index // 64  # start 좌표
        b = index % 64  # end 좌표

        startAlphabet = a // 8  # a~h 를 나타내는 숫자
        startNumber = a % 8  # 1~8을 나타내는 숫자

        endAlphabet = b // 8  # a~h 를 나타내는 숫자
        endNumber = b % 8  # 1~8을 나타내는 숫자
        return row1[startAlphabet] + colomn1[startNumber] + row1[endAlphabet] + colomn1[endNumber]
