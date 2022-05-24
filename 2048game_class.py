import pygame,sys,time
from pygame.locals import *
from constants import *
from random import *

# colors
black = (0,0,0)
red = (255,0,0)
orange = (255,152,0)
deeporange = (255,87,34)
brown = (121,85,72)
green = (0,128,0)
lgreen = (139,195,74)
teal = (0,150,136)
blue  = (33,150,136)
purple = (156,39,176)
pink = (234,30,99)
deepurple = (103,58,183)


colordict = {
    0:black,
    2:red,
    4:green,
    8:purple,
    16:deepurple,
    32:deeporange,
    64:teal,
    128:lgreen,
    256:pink,
    512:orange,
    1024:black,
    2048:brown
}
def getcolor(i):
    return colordict[i]

class MyGame:
    def __init__(self):
        self.sizeofboard = 4
        self.totalpoints = 0
        self.defaultscore = 2

        self.tileofmatrix = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        self.undomatrix = []

        pygame.init()

        self.surface = pygame.display.set_mode((400,500),0,32)
        pygame.display.set_caption("2048 Game")

        self.font = pygame.font.SysFont("monospace",40)
        self.fontofscore = pygame.font.SysFont("monospace",30)

    def canmove(self):
        for i in range(0,self.sizeofboard):
            for j in range(1,self.sizeofboard):
                if self.tileofmatrix[i][j-1] == 0 and self.tileofmatrix[i][j] > 0:
                    return True 
                elif (self.tileofmatrix[i][j-1] == self.tileofmatrix[i][j]) and self.tileofmatrix[i][j-1] != 0:
                    return True
        return False
        
    def movetiles(self):
        for i in range(0,self.sizeofboard):
            for j in range(0,self.sizeofboard-1):
                
                while self.tileofmatrix[i][j] == 0 and sum(self.tileofmatrix[i][j:]) > 0:
                    for k in range(j,self.sizeofboard-1):
                        self.tileofmatrix[i][k] = self.tileofmatrix[i][k+1]
                        self.tileofmatrix[i][self.sizeofboard-1] = 0

    def mergetiles(self):
        for i in range(0,self.sizeofboard):
            for k in range(0,self.sizeofboard-1):
                if self.tileofmatrix[i][k] == self.tileofmatrix[i][k+1] and self.tileofmatrix[i][k] != 0:
                    self.tileofmatrix[i][k] = self.tileofmatrix[i][k]*2
                    self.tileofmatrix[i][k+1] = 0 
                    self.totalpoints+= self.tileofmatrix[i][k]
                    self.movetiles()

    def placerandomtile(self):
        c = 0
        for i in range(0,self.sizeofboard):
            for j in range(0,self.sizeofboard):
                if self.tileofmatrix[i][j] == 0:
                    c += 1
        
        k = self.floor(random() * self.sizeofboard* self.sizeofboard)
        print("click")

        while self.tileofmatrix[self.floor(k/self.sizeofboard)][k%self.sizeofboard] != 0:
            k = self.floor(random() * self.sizeofboard * self.sizeofboard)

        self.tileofmatrix[self.floor(k/self.sizeofboard)][k%self.sizeofboard] = 2

    def floor(self, n):
        return int(n - (n % 1 ))  

    def printmatrix(self):
            self.surface.fill(black)

            for i in range(0,self.sizeofboard):
                for j in range(0,self.sizeofboard):
                    pygame.draw.rect(self.surface,getcolor(self.tileofmatrix[i][j]),(i*(400/self.sizeofboard),j*(400/self.sizeofboard)+100,400/self.sizeofboard,400/self.sizeofboard))
                    label = self.font.render(str(self.tileofmatrix[i][j]),1,(255,255,255))
                    label2 = self.fontofscore.render("YourScore:"+str(self.totalpoints),1,(255,255,255))
                    self.surface.blit(label,(i*(400/self.sizeofboard)+30,j*(400/self.sizeofboard)+130))
                    self.surface.blit(label2,(10,20))



    def checkIfCanGo(self):
        for i in range(0,self.sizeofboard ** 2): 
            if self.tileofmatrix[self.floor(i/self.sizeofboard)][i%self.sizeofboard] == 0:
                return True
        
        for i in range(0,self.sizeofboard):
            for j in range(0,self.sizeofboard-1):
                if self.tileofmatrix[i][j] == self.tileofmatrix[i][j+1]:
                    return True
                elif self.tileofmatrix[j][i] ==self.tileofmatrix[j+1][i]:
                    return True
        return False

    
    def convertToLinearMatrix(self):

        mat = []
        for i in range(0,self.sizeofboard ** 2):
            mat.append(self.tileofmatrix[self.floor(i/self.sizeofboard)][i%self.sizeofboard])

        mat.append(self.totalpoints)
        return mat


    def addToUndo(self):
        self.undomatrix.append(self.convertToLinearMatrix())   

    def rotatematrixclockwise(self):
        for i in range(0,int(self.sizeofboard/2)):
            for k in range(i,self.sizeofboard- i- 1):
                temp1 = self.tileofmatrix[i][k]
                temp2 = self.tileofmatrix[self.sizeofboard - 1 - k][i]
                temp3 = self.tileofmatrix[self.sizeofboard- 1 - i][self.sizeofboard - 1 - k]
                temp4 = self.tileofmatrix[k][self.sizeofboard- 1 - i]

                self.tileofmatrix[self.sizeofboard- 1 - k][i] = temp1
                self.tileofmatrix[self.sizeofboard - 1 - i][self.sizeofboard - 1 - k] = temp2
                self.tileofmatrix[k][self.sizeofboard - 1 - i] = temp3
                self.tileofmatrix[i][k] = temp4


    def gameover(self):
        self.surface.fill(black)

        label = self.font.render("gameover",1,(255,255,255))
        label2 =self.font.render("score : "+str(self.totalpoints),1,(255,255,255))
        label3 = self.font.render("press 'R' to play again",1,(255,255,255))

        self.surface.blit(label,(50,100))
        self.surface.blit(label2,(50,200))
        self.surface.blit(label3,(50,300))


    def reset(self):
        self.totalpoints= 0
        self.surface.fill(black)
        self.tileofmatrix = [[0 for i in range(0,self.sizeofboard)] for j in range(0,self.sizeofboard) ]
        self.main()

    def undo(self):
        if len(self.undomatrix) > 0:
            mat = self.undomatrix.pop()

            for i in range(0,self.sizeofboard ** 2):
                self.tileofmatrix[self.floor(i/self.sizeofboard)][i%self.sizeofboard] = mat[i]
            self.totalpoints = mat[self.sizeofboard ** 2]

            self.printmatrix()

    def isArrow(self, k):
        return (k == pygame.K_UP or k == pygame.K_DOWN or k == pygame.K_LEFT or k == pygame.K_RIGHT)

    def getrotations(self, k):
        if k == pygame.K_UP:
            return 0
        elif k == pygame.K_DOWN:
            return 2 
        elif k == pygame.K_LEFT:
            return 1
        elif k == pygame.K_RIGHT:
            return 3

    def main(self):
        # start with two tiles
        self.placerandomtile()
        self.placerandomtile()
        self.printmatrix()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                
                if self.checkIfCanGo() == True:
                    if event.type == KEYDOWN:
                        if self.isArrow(event.key):
                            rotations = self.getrotations(event.key)
                            self.addToUndo()
                            for i in range(0,rotations):
                                self.rotatematrixclockwise()

                            if self.canmove():
                                self.movetiles()
                                self.mergetiles()
                                self.placerandomtile()

                            for j in range(0,(4-rotations)%4):
                                self.rotatematrixclockwise()
                                
                            self.printmatrix()
                else: 
                    self.gameover()

                if event.type == KEYDOWN:
                    global sizeofboard

                    if event.key == pygame.K_r:
                    
                        self.reset()
                    if 50<event.key and 56 > event.key:
                        
                        sizeofboard = event.key - 48
                        self.reset()
                        
                    elif event.key == pygame.K_u:
                        self.undo()
                    
            pygame.display.update()

if __name__ == "__main__":
    mgame = MyGame()
    MyGame.main(mgame)  