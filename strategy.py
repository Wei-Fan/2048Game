import numpy as np

class myBot:
    move_order = [2, 3, 1, 0] # 0: up 1:left 2:down 3:right
    my_move = 0

    def __init__(self):
        pass


    def readBoard(self, tileofmatrix):
        # print to terminal
        print("-----------------")
        _mat = np.array(tileofmatrix)
        print(np.transpose(_mat))


    def resetMove(self):
        self.my_move = 0


    def changeDirection(self):
        self.my_move = (self.my_move + 1) % 4


    def playAMove(self):
        return self.move_order[self.my_move]