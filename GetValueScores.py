import chess
import numpy as np
import tensorflow as tf
import os

from Board2Array import Board2Array as B2A
from OneHotEncoding import OneHotEncode as OHE

class GetValueScores:
    def __init__(self):
        #입력으로 체스 보드를 받아온다

        self.promotion = 0.5 # legalmoves중에서 몇 퍼센트까지 만들지 결정 비율
        self.penalty = 0.01 # Score계산에서
        self.madeMoves = [] # 선택된 Moves의 list
        self.madeMovesScores =[] # madeMoves의 점수들이 들어 있는 list
        self.flag = False
        self.sess = tf.Session()
        with tf.variable_scope("ValueNetwork",reuse=False):
            self.X = tf.placeholder(tf.float32, [None, 8, 8, 16], name="X")  # 체스에서 8X8X10 이미지를 받기 위해 64

            self.W1 = tf.get_variable("W1", shape=[1, 1, 16, 128], initializer=tf.contrib.layers.xavier_initializer())
            self.B1 = tf.get_variable("B1", initializer=tf.random_normal([128], stddev=0.01))
            self.L1 = tf.nn.relu(tf.nn.conv2d(self.X, self.W1, strides=[1, 1, 1, 1], padding='SAME') + self.B1)

            self.W2 = tf.get_variable("W2", shape=[3, 3, 128, 128], initializer=tf.contrib.layers.xavier_initializer())
            self.B2 = tf.get_variable("B2", initializer=tf.random_normal([128], stddev=0.01))
            self. L2 = tf.nn.relu(tf.nn.conv2d(self.L1, self.W2, strides=[1, 1, 1, 1], padding='SAME') + self.B2)

            self.W3 = tf.get_variable("W3", shape=[3, 3, 128, 128], initializer=tf.contrib.layers.xavier_initializer())
            self.B3 = tf.get_variable("B3", initializer=tf.random_normal([128], stddev=0.01))
            self.L3 = tf.nn.relu(tf.nn.conv2d(self.L2, self.W3, strides=[1, 1, 1, 1], padding='VALID') + self.B3)

            self.FlatLayer = tf.reshape(self.L3, [-1, 6 * 6 * 128])
            self.Flat_W = tf.get_variable("Flat_W", shape=[6 * 6 * 128, 256], initializer=tf.contrib.layers.xavier_initializer())
            self.Flat_B = tf.get_variable("Flat_B", initializer=tf.random_normal([256], stddev=0.01))
            self.Flat_L = tf.nn.relu(tf.matmul(self.FlatLayer, self.Flat_W) + self.Flat_B)

            self.Flat_W2 = tf.get_variable("Flat_W2", initializer=tf.truncated_normal([256, 4], stddev=0.01))
            self.Flat_B2 = tf.get_variable("Flat_B2", initializer=tf.random_normal([4], stddev=0.01))

            self.hypothesis = tf.matmul(self.Flat_L, self.Flat_W2) + self.Flat_B2

            self.SMhy = tf.nn.softmax(self.hypothesis)

            tf.get_variable_scope().reuse_variables() # 변수를 재사용하기 위한 방법
            self.flag =True
            self.sess.run(tf.global_variables_initializer())


        saver = tf.train.Saver()
        print(os.path)
        ckpt = tf.train.get_checkpoint_state(os.path.dirname('./VNCheckpoint/'))
        print("asdasd",ckpt.model_checkpoint_path)
        if ckpt and ckpt.model_checkpoint_path:
            print("asdasd")
            #print(ckpt.model_checkpoint_path)
            saver.restore(self.sess, ckpt.model_checkpoint_path)
            #print("\n체크포인트 파일 재사용 = ", ckpt.model_checkpoint_path)
        del(ckpt)
        del(saver)

    def get_Model(self,startCnnInput):

        getSoftmax = self.sess.run(self.SMhy, feed_dict = {self.X:startCnnInput})
        return getSoftmax

    def makeStartInput(self, chessBoard):

        startCnnInput = []
        startCnnInput.append(B2A().board2array4(chessBoard))
        print(np.shape(startCnnInput))
        startCnnInput = np.reshape(startCnnInput, [-1, 8, 8, 16])
        #startCnnInput = tf.to_float(startCnnInput)

        return startCnnInput

    def makeScores(self,chessBoard):
        startCnnInput= self.makeStartInput(chessBoard)
        softMax = self.get_Model(startCnnInput)
        softMax = np.array(softMax[0])

        return softMax

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
