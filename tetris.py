#Tetris Game, written in Python 3.6.5
#Version: 1.0
#Date: 26.05.2018

import pygame #version 1.9.3
import random
import math
import sys

from Mat import Mat
from Result import Result
from CurrentPiece import CurrentPiece
from MyCallback import MyCallback



from specializations.dlv2.desktop.dlv2_desktop_service import DLV2DesktopService
from platforms.desktop.desktop_handler import DesktopHandler
from languages.asp.asp_input_program import ASPInputProgram
from languages.asp.asp_mapper import ASPMapper





pygame.init()
pygame.font.init()

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT))
pygame.display.set_caption('Tetris')
clock = pygame.time.Clock()

pieceNames = ('I', 'O', 'T', 'S', 'Z', 'J', 'L')

print(pieceNames[0].lower())

STARTING_LEVEL = 0 #Change this to start a new game at a higher level

MOVE_PERIOD_INIT = 4 #Piece movement speed when up/right/left arrow keys are pressed (Speed is defined as frame count. Game is 60 fps) 

CLEAR_ANI_PERIOD = 4 #Line clear animation speed
SINE_ANI_PERIOD = 120 #Sine blinking effect speed

#Font sizes
SB_FONT_SIZE = 20
FONT_SIZE_SMALL = 15
PAUSE_FONT_SIZE = 66
GAMEOVER_FONT_SIZE = 66
TITLE_FONT_SIZE = 65
VERSION_FONT_SIZE = 20

fontSB = pygame.font.Font('Gameplay.ttf', SB_FONT_SIZE)
fontSmall = pygame.font.Font('Gameplay.ttf', FONT_SIZE_SMALL)
fontPAUSE = pygame.font.Font('Gameplay.ttf', PAUSE_FONT_SIZE)
fontGAMEOVER = pygame.font.Font('Gameplay.ttf', GAMEOVER_FONT_SIZE)
fontTitle = pygame.font.Font('Gameplay.ttf', TITLE_FONT_SIZE)
fontVersion = pygame.font.SysFont('arial', VERSION_FONT_SIZE)

ROW = (0)
COL = (1)

#Some color definitions
BLACK = (0,0,0)
WHITE = (255,255,255)
DARK_GRAY = (80,80,80)
GRAY = (110,110,110)
LIGHT_GRAY = (150,150,150)
BORDER_COLOR = GRAY
NUM_COLOR = WHITE
TEXT_COLOR = GRAY

blockColors = {
'I' : (19,232,232), #CYAN
'O' : (236,236,14), #YELLOW
'T' : (126,5,126), #PURPLE
'S' : (0,128,0), #GREEN
'Z' : (236,14,14), #RED
'J' : (30,30,201), #BLUE
'L' : (240,110,2) } #ORANGE

#Initial(spawn) block definitons of each piece
pieceDefs = {
'I' : ((1,0),(1,1),(1,2),(1,3)),
'O' : ((0,1),(0,2),(1,1),(1,2)),
'T' : ((0,1),(1,0),(1,1),(1,2)),
'S' : ((0,1),(0,2),(1,0),(1,1)),
'Z' : ((0,0),(0,1),(1,1),(1,2)),
'J' : ((0,0),(1,0),(1,1),(1,2)),
'L' : ((0,2),(1,0),(1,1),(1,2)) }

directions = {
'down' : (1,0),
'right' : (0,1),
'left' : (0,-1),
'downRight' : (1,1),
'downLeft' : (1,-1),
'noMove' : (0,0) }

levelSpeeds = (48,43,38,33,28,23,18,13,8,6,5,5,5,4,4,4,3,3,3,2,2,2,2,2,2,2,2,2,2)
#The speed of the moving piece at each level. Level speeds are defined as levelSpeeds[level]
#Each 10 cleared lines means a level up.
#After level 29, speed is always 1. Max level is 99

baseLinePoints = (0,40,100,300,1200)
#Total score is calculated as: Score = level*baseLinePoints[clearedLineNumberAtATime] + totalDropCount
#Drop means the action the player forces the piece down instead of free fall(By key combinations: down, down-left, down-rigth arrows)



class AiHandler():

   

    def __init__(self):
        self.handler = DesktopHandler(DLV2DesktopService("lib/dlv-2.1.1-win64.exe"))
    
        ASPMapper.get_instance().register_class(Mat)
        ASPMapper.get_instance().register_class(CurrentPiece)
        ASPMapper.get_instance().register_class(Result)
        
        self.fixedProgram = ASPInputProgram()
        self.variableProgram = ASPInputProgram()
        
        

        self.fixedProgram.add_files_path("encodings/strategia2.asp")
        

        self.handler.add_program(self.fixedProgram)
        self.handler.add_program(self.variableProgram)
        
        

    def changeVariableProgram(self,matrix,currentPiece):
            
            for i in range(len(matrix)):
                    for j in range(len(matrix[0])):
                          self.variableProgram.add_object_input(Mat(i,j,matrix[i][j]))
            c = CurrentPiece(currentPiece)
            self.variableProgram.add_object_input(c)
            
            
            
    
    def execute(self,mainBoard):
        c = MyCallback(mainBoard)
        return self.handler.start_async(c)
                      
    def clearVariableProgram(self):
          self.variableProgram.clear_all()






#Class implementing random generator algorithm	

class RandomGenerator:
    def __init__(self):
        self.bag = []
        self.refill_bag()
    
    def refill_bag(self):
        self.bag = [0,1,2,3,4,5,6]
        #self.bag=[3]
        random.shuffle(self.bag)
    
    def get_next_piece(self):
        if len(self.bag) == 0:
            self.refill_bag()
        return self.bag.pop(0)
    

#Class for the game's timing events
class GameClock:
    
    def __init__(self):
        self.frameTick = 0 #The main clock tick of the game, increments at each frame (1/60 secs, 60 fps)
        self.pausedMoment = 0
        self.move = self.TimingType(MOVE_PERIOD_INIT) #Drop and move(right and left) timing object
        self.fall = self.TimingType(levelSpeeds[STARTING_LEVEL]) #Free fall timing object
        self.clearAniStart = 0
    
    class TimingType:
        
        def __init__(self,framePeriod):
            self.preFrame = 0
            self.framePeriod = framePeriod
            
        def check(self,frameTick):
            if frameTick - self.preFrame > self.framePeriod - 1:
                self.preFrame = frameTick
                return True
            return False
    
    def pause(self):
        self.pausedMoment = self.frameTick
    
    def unpause(self):
        self.frameTick = self.pausedMoment
    
    def restart(self):
        self.frameTick = 0
        self.pausedMoment = 0
        self.move = self.TimingType(MOVE_PERIOD_INIT)
        self.fall = self.TimingType(levelSpeeds[STARTING_LEVEL])
        self.clearAniStart = 0
        
    def update(self):
        self.frameTick = self.frameTick + 1
    
    def speedup(self):
        self.fall = self.TimingType(1)
        

# Class for all the game mechanics, visuals and events
class MainBoard:

    def __init__(self,blockSize,xPos,yPos,colNum,rowNum,boardLineWidth,blockLineWidth,scoreBoardWidth):
        
        #Size and position initiations
        self.blockSize = blockSize
        self.xPos = xPos
        self.yPos = yPos
        self.colNum = colNum
        self.rowNum = rowNum
        self.boardLineWidth = boardLineWidth
        self.blockLineWidth = blockLineWidth
        self.scoreBoardWidth = scoreBoardWidth
        self.randomGenerator = RandomGenerator()
        self.matrix = [[0] * colNum for i in range(rowNum)]
        self.currentPiece = None
        self.newPiece = False #new piece arrived
        self.step = 0
        
        #Matrix that contains all the existing blocks in the game board, except the moving piece
        self.blockMat = [['empty'] * colNum for i in range(rowNum)]
        
        self.piece = MovingPiece(colNum,rowNum,'uncreated')
        
        self.lineClearStatus = 'idle' # 'clearRunning' 'clearFin'
        self.clearedLines = [-1,-1,-1,-1]
        
        self.gameStatus = 'firstStart' # 'running' 'gameOver'
        self.gamePause = False
        self.nextPieces = ['I','I']
        
        self.score = 0
        self.level = STARTING_LEVEL
        self.lines = 0
    
    def restart(self):
        self.blockMat = [['empty'] * self.colNum for i in range(self.rowNum)]
        self.matrix = [[0] * self.colNum for i in range(self.rowNum)]
        self.piece = MovingPiece(self.colNum,self.rowNum,'uncreated')
        
        self.lineClearStatus = 'idle'
        self.clearedLines = [-1,-1,-1,-1]		
        gameClock.fall.preFrame = gameClock.frameTick
        self.generateNextTwoPieces()
        self.gameStatus = 'running'
        self.gamePause = False
        
        self.score = 0
        self.level = STARTING_LEVEL
        self.lines = 0
        
        gameClock.restart()
        
    def erase_BLOCK(self,xRef,yRef,row,col):
        pygame.draw.rect(gameDisplay, BLACK, [xRef+(col*self.blockSize),yRef+(row*self.blockSize),self.blockSize,self.blockSize],0)
        
    def draw_BLOCK(self,xRef,yRef,row,col,color):
        pygame.draw.rect(gameDisplay, BLACK, [xRef+(col*self.blockSize),yRef+(row*self.blockSize),self.blockSize,self.blockLineWidth],0)
        pygame.draw.rect(gameDisplay, BLACK, [xRef+(col*self.blockSize)+self.blockSize-self.blockLineWidth,yRef+(row*self.blockSize),self.blockLineWidth,self.blockSize],0)
        pygame.draw.rect(gameDisplay, BLACK, [xRef+(col*self.blockSize),yRef+(row*self.blockSize),self.blockLineWidth,self.blockSize],0)
        pygame.draw.rect(gameDisplay, BLACK, [xRef+(col*self.blockSize),yRef+(row*self.blockSize)+self.blockSize-self.blockLineWidth,self.blockSize,self.blockLineWidth],0)

        pygame.draw.rect(gameDisplay, color, [xRef+(col*self.blockSize)+self.blockLineWidth,yRef+(row*self.blockSize)+self.blockLineWidth,self.blockSize-(2*self.blockLineWidth),self.blockSize-(2*self.blockLineWidth)],0)
    
    def draw_GAMEBOARD_BORDER(self):
        pygame.draw.rect(gameDisplay, BORDER_COLOR, [self.xPos-self.boardLineWidth-self.blockLineWidth,self.yPos-self.boardLineWidth-self.blockLineWidth,(self.blockSize*self.colNum)+(2*self.boardLineWidth)+(2*self.blockLineWidth),self.boardLineWidth],0)
        pygame.draw.rect(gameDisplay, BORDER_COLOR, [self.xPos+(self.blockSize*self.colNum)+self.blockLineWidth,self.yPos-self.boardLineWidth-self.blockLineWidth,self.boardLineWidth,(self.blockSize*self.rowNum)+(2*self.boardLineWidth)+(2*self.blockLineWidth)],0)
        pygame.draw.rect(gameDisplay, BORDER_COLOR, [self.xPos-self.boardLineWidth-self.blockLineWidth,self.yPos-self.boardLineWidth-self.blockLineWidth,self.boardLineWidth,(self.blockSize*self.rowNum)+(2*self.boardLineWidth)+(2*self.blockLineWidth)],0)
        pygame.draw.rect(gameDisplay, BORDER_COLOR, [self.xPos-self.boardLineWidth-self.blockLineWidth,self.yPos+(self.blockSize*self.rowNum)+self.blockLineWidth,(self.blockSize*self.colNum)+(2*self.boardLineWidth)+(2*self.blockLineWidth),self.boardLineWidth],0)
    
    def draw_GAMEBOARD_CONTENT(self):
    
        """if self.gameStatus == 'firstStart':	
            
            titleText = fontTitle.render('TETRIS', False, WHITE)
            gameDisplay.blit(titleText,(self.xPos++1.55*self.blockSize,self.yPos+8*self.blockSize))
            
            versionText = fontVersion.render('v 1.0', False, WHITE)
            gameDisplay.blit(versionText,(self.xPos++7.2*self.blockSize,self.yPos+11.5*self.blockSize))
            
        else:"""
        for row in range(0,self.rowNum):
            for col in range(0,self.colNum):
                if self.blockMat[row][col] == 'empty':
                    self.erase_BLOCK(self.xPos,self.yPos,row,col)
                else:
                    self.draw_BLOCK(self.xPos,self.yPos,row,col,blockColors[self.blockMat[row][col]])
                        
            if self.piece.status == 'moving':
                for i in range(0,4):
                    self.draw_BLOCK(self.xPos,self.yPos,self.piece.blocks[i].currentPos.row, self.piece.blocks[i].currentPos.col, blockColors[self.piece.type])
                    
            if self.gamePause == True:
                #pygame.draw.rect(gameDisplay, DARK_GRAY, [self.xPos+1*self.blockSize,self.yPos+8*self.blockSize,8*self.blockSize,4*self.blockSize],0)
                pauseText = fontPAUSE.render('PAUSE', False, WHITE)
                gameDisplay.blit(pauseText,(self.xPos++1.65*self.blockSize,self.yPos+8*self.blockSize))
            
            if self.gameStatus == 'gameOver':
                pygame.draw.rect(gameDisplay, LIGHT_GRAY, [self.xPos+1*self.blockSize,self.yPos+8*self.blockSize,8*self.blockSize,8*self.blockSize],0)
                gameOverText0 = fontGAMEOVER.render('GAME', False, BLACK)
                gameDisplay.blit(gameOverText0,(self.xPos++2.2*self.blockSize,self.yPos+8*self.blockSize))
                gameOverText1 = fontGAMEOVER.render('OVER', False, BLACK)
                gameDisplay.blit(gameOverText1,(self.xPos++2.35*self.blockSize,self.yPos+12*self.blockSize))
            
        
        
    def draw_SCOREBOARD_BORDER(self):
        pygame.draw.rect(gameDisplay, BORDER_COLOR, [self.xPos+(self.blockSize*self.colNum)+self.blockLineWidth,self.yPos-self.boardLineWidth-self.blockLineWidth,self.scoreBoardWidth+self.boardLineWidth,self.boardLineWidth],0)
        pygame.draw.rect(gameDisplay, BORDER_COLOR, [self.xPos+(self.blockSize*self.colNum)+self.boardLineWidth+self.blockLineWidth+self.scoreBoardWidth,self.yPos-self.boardLineWidth-self.blockLineWidth,self.boardLineWidth,(self.blockSize*self.rowNum)+(2*self.boardLineWidth)+(2*self.blockLineWidth)],0)
        pygame.draw.rect(gameDisplay, BORDER_COLOR, [self.xPos+(self.blockSize*self.colNum)+self.blockLineWidth,self.yPos+(self.blockSize*self.rowNum)+self.blockLineWidth,self.scoreBoardWidth+self.boardLineWidth,self.boardLineWidth],0)
    
    def draw_SCOREBOARD_CONTENT(self):
        
        xPosRef = self.xPos+(self.blockSize*self.colNum)+self.boardLineWidth+self.blockLineWidth
        yPosRef = self.yPos
        yLastBlock = self.yPos+(self.blockSize*self.rowNum)
    
        if self.gameStatus == 'running':
            nextPieceText = fontSB.render('next:', False, TEXT_COLOR)
            gameDisplay.blit(nextPieceText,(xPosRef+self.blockSize,self.yPos+10))
            
            blocks = [[0,0],[0,0],[0,0],[0,0]]
            origin = [0,0]
            for i in range(0,4):
                blocks[i][ROW] = origin[ROW] + pieceDefs[self.nextPieces[1]][i][ROW]
                blocks[i][COL] = origin[COL] + pieceDefs[self.nextPieces[1]][i][COL]
                
                if self.nextPieces[1] == 'O':
                    self.draw_BLOCK(xPosRef+0.5*self.blockSize,yPosRef+2.25*self.blockSize+15,blocks[i][ROW],blocks[i][COL],blockColors[self.nextPieces[1]])
                elif self.nextPieces[1] == 'I':
                    self.draw_BLOCK(xPosRef+0.5*self.blockSize,yPosRef+1.65*self.blockSize+15,blocks[i][ROW],blocks[i][COL],blockColors[self.nextPieces[1]])
                else:
                    self.draw_BLOCK(xPosRef+1*self.blockSize,yPosRef+2.25*self.blockSize+15,blocks[i][ROW],blocks[i][COL],blockColors[self.nextPieces[1]])
            
            """
            if self.gamePause == False:
                pauseText = fontSmall.render('P -> pause', False, WHITE)
                gameDisplay.blit(pauseText,(xPosRef+1*self.blockSize,yLastBlock-15*self.blockSize))
            else:
                unpauseText = fontSmall.render('P -> unpause', False, self.whiteSineAnimation())
                gameDisplay.blit(unpauseText,(xPosRef+1*self.blockSize,yLastBlock-15*self.blockSize))
                
            restartText = fontSmall.render('R -> restart', False, WHITE)
            gameDisplay.blit(restartText,(xPosRef+1*self.blockSize,yLastBlock-14*self.blockSize))
            """
        
        pygame.draw.rect(gameDisplay, BORDER_COLOR, [xPosRef,yLastBlock-12.5*self.blockSize,self.scoreBoardWidth,self.boardLineWidth],0)
        
        scoreText = fontSB.render('score:', False, TEXT_COLOR)
        gameDisplay.blit(scoreText,(xPosRef+self.blockSize-10,yLastBlock-12*self.blockSize))
        scoreNumText = fontSB.render(str(self.score), False, NUM_COLOR)
        gameDisplay.blit(scoreNumText,(xPosRef+self.blockSize-10,yLastBlock-10*self.blockSize))
        
        levelText = fontSB.render('level:', False, TEXT_COLOR)
        gameDisplay.blit(levelText,(xPosRef+self.blockSize-10,yLastBlock-8*self.blockSize))
        levelNumText = fontSB.render(str(self.level), False, NUM_COLOR)
        gameDisplay.blit(levelNumText,(xPosRef+self.blockSize-10,yLastBlock-6*self.blockSize))
        
        linesText = fontSB.render('lines:', False, TEXT_COLOR)
        gameDisplay.blit(linesText,(xPosRef+self.blockSize-10,yLastBlock-4*self.blockSize))
        linesNumText = fontSB.render(str(self.lines), False, NUM_COLOR)
        gameDisplay.blit(linesNumText,(xPosRef+self.blockSize-10,yLastBlock-2*self.blockSize))
    
    # All the screen drawings occurs in this function, called at each game loop iteration
    def draw(self):
        
        self.draw_GAMEBOARD_BORDER()
        self.draw_SCOREBOARD_BORDER()
        
        self.draw_GAMEBOARD_CONTENT()
        self.draw_SCOREBOARD_CONTENT()
        
    def whiteSineAnimation(self):
        
        sine = math.floor(255 * math.fabs(math.sin(2*math.pi*(gameClock.frameTick/(SINE_ANI_PERIOD*2)))))
        #sine = 127 + math.floor(127 * math.sin(2*math.pi*(gameClock.frameTick/SINE_ANI_PERIOD)))
        sineEffect = [sine,sine,sine]
        return sineEffect
    
    def lineClearAnimation(self):
    
        clearAniStage = math.floor((gameClock.frameTick - gameClock.clearAniStart)/CLEAR_ANI_PERIOD)
        halfCol = math.floor(self.colNum/2)
        if clearAniStage < halfCol:
            for i in range(0,4):
                if self.clearedLines[i] >= 0:
                    self.blockMat[self.clearedLines[i]][(halfCol)+clearAniStage] = 'empty'
                    self.blockMat[self.clearedLines[i]][(halfCol-1)-clearAniStage] = 'empty'
                    self.matrix[self.clearedLines[i]][(halfCol)+clearAniStage] = 0
                    self.matrix[self.clearedLines[i]][(halfCol-1)-clearAniStage] = 0
        else:
            self.lineClearStatus = 'cleared'
    
    def dropFreeBlocks(self): #Drops down the floating blocks after line clears occur
        
        for cLIndex in range(0,4):
            if self.clearedLines[cLIndex] >= 0:
                for rowIndex in range(self.clearedLines[cLIndex],0,-1):
                    for colIndex in range(0,self.colNum):
                        self.blockMat[rowIndex+cLIndex][colIndex] = self.blockMat[rowIndex+cLIndex-1][colIndex]
                        self.matrix[rowIndex+cLIndex][colIndex] = self.matrix[rowIndex+cLIndex-1][colIndex] 
                
                for colIndex in range(0,self.colNum):
                    self.blockMat[0][colIndex] = 'empty'
                    self.matrix[0][colIndex] = 0
    
    def getCompleteLines(self): #Returns index list(length of 4) of cleared lines(-1 if not assigned as cleared line)
        
        clearedLines = [-1,-1,-1,-1]
        cLIndex = -1
        rowIndex = self.rowNum - 1
        
        while rowIndex >= 0:
            for colIndex in range(0,self.colNum):
                if self.blockMat[rowIndex][colIndex] == 'empty':
                    rowIndex = rowIndex - 1
                    break
                if colIndex == self.colNum - 1:
                    cLIndex = cLIndex + 1
                    clearedLines[cLIndex] = rowIndex
                    rowIndex = rowIndex - 1

        if cLIndex >= 0:
            gameClock.clearAniStart = gameClock.frameTick
            self.lineClearStatus = 'clearRunning'
        else:
            self.prepareNextSpawn()
            
        return clearedLines
    
    def prepareNextSpawn(self):
        self.generateNextPiece()
        self.lineClearStatus = 'idle'
        self.piece.status = 'uncreated'
    
    def generateNextTwoPieces(self):
        self.nextPieces[0] = pieceNames[self.randomGenerator.get_next_piece()]
        self.nextPieces[1] = pieceNames[self.randomGenerator.get_next_piece()]
        self.piece.type = self.nextPieces[0]
        c = self.nextPieces[0].lower()
        self.currentPiece=c
        
    def generateNextPiece(self):
        self.nextPieces[0] = self.nextPieces[1]
        self.nextPieces[1] = pieceNames[self.randomGenerator.get_next_piece()]
        self.piece.type = self.nextPieces[0]
        c = self.nextPieces[0].lower()
        self.step = 0
        self.currentPiece=c
    
    def isNewPiece(self):
        return self.newPiece

    def setNewPiece(self):
        self.newPiece = False

    def printMatrix(self):
        print("STEP")
        for i in range(0,self.rowNum):
            for j in range(0,self.colNum):
                print(self.matrix[i][j], end= " ")
            print("\n")
            

    def checkAndApplyGameOver(self):
        if self.piece.gameOverCondition == True:
            self.gameStatus = 'gameOver'
            for i in range(0,4):
                if self.piece.blocks[i].currentPos.row >= 0 and self.piece.blocks[i].currentPos.col >= 0:
                    self.blockMat[self.piece.blocks[i].currentPos.row][self.piece.blocks[i].currentPos.col] = self.piece.type
                    self.matrix[self.piece.blocks[i].currentPos.row][self.piece.blocks[i].currentPos.col] = 1
    
    
    def updateScores(self):
        
        clearedLinesNum = 0
        for i in range(0,4):
            if self.clearedLines[i] > -1:
                clearedLinesNum = clearedLinesNum + 1
                
        self.score = self.score + (self.level+1)*baseLinePoints[clearedLinesNum] + self.piece.dropScore
        self.lines = self.lines + clearedLinesNum
        self.level = STARTING_LEVEL + math.floor(self.lines/10)
    
    def updateSpeed(self):
    
        if self.level < 29:
            gameClock.fall.framePeriod = levelSpeeds[self.level]
        else:
            gameClock.fall.framePeriod = 1
            
        if gameClock.fall.framePeriod < 4:
            gameClock.fall.framePeriod = gameClock.move.framePeriod
    
    # All the game events and mechanics are placed in this function, called at each game loop iteration
    def gameAction(self):

        if self.gameStatus == 'firstStart':
            self.restart()
        
        if self.step == 1: #when the first step occurs,new piece
            self.newPiece = True 
        self.piece.move(self.blockMat,False,False)
        self.checkAndApplyGameOver()
        self.step+=1

        if self.gameStatus != 'gameOver':
            if self.piece.status == 'moving':
                pass
            if self.piece.status == 'collided':		
                if self.lineClearStatus == 'idle':
                    for i in range(0,4):
                        self.blockMat[self.piece.blocks[i].currentPos.row][self.piece.blocks[i].currentPos.col] = self.piece.type
                        self.matrix[self.piece.blocks[i].currentPos.row][self.piece.blocks[i].currentPos.col] = 1
                    self.clearedLines = self.getCompleteLines()
                    self.updateScores()
                    self.updateSpeed()
                elif self.lineClearStatus == 'clearRunning':
                    self.lineClearAnimation()
                else: # 'clearFin'
                    self.dropFreeBlocks()					
                    self.prepareNextSpawn()

    def move(self,right,left,number):
        for i in range(number):
            self.piece.move(self.blockMat,right,left)

    def rotate(self,rotationNumber):
        min = 3
        for i in range(0,rotationNumber):
            min = self.piece.rotate()
        return min


    def getMatrix(self):
        return self.matrix

    def drop(self):
        self.piece.drop()

    def prt(self):
        self.piece.prt()
    
    def getCurrentPiece(self):
        return self.currentPiece
                
# Class for all the definitions of current moving piece
class MovingPiece:

    def __init__(self,colNum,rowNum,status):

        self.colNum = colNum
        self.rowNum = rowNum

        self.blockMat = [['empty'] * colNum for i in range(rowNum)]
        
        self.blocks = []
        for i in range(0,4):
            self.blocks.append(MovingBlock())
        
        self.currentDef = [[0] * 2 for i in range(4)]
        self.status = status # 'uncreated' 'moving' 'collided'
        self.type = 'I' # 'O', 'T', 'S', 'Z', 'J', 'L'
        
        self.gameOverCondition = False
        
        self.dropScore = 0
        self.lastMoveType = 'noMove'
    
    def applyNextMove(self):
        for i in range(0,4):
            self.blocks[i].currentPos.col = self.blocks[i].nextPos.col
            self.blocks[i].currentPos.row = self.blocks[i].nextPos.row
    
    def applyFastMove(self):
        
        if gameClock.move.check(gameClock.frameTick) == True:
            if self.lastMoveType == 'downRight' or self.lastMoveType == 'downLeft' or self.lastMoveType == 'down':
                self.dropScore = self.dropScore + 1
            self.applyNextMove()
            
    def slowMoveAction(self):
    
        if gameClock.fall.check(gameClock.frameTick) == True:
            if self.movCollisionCheck('down') == True:
                self.createNextMove('noMove')
                self.status = 'collided'
            else:
                self.createNextMove('down')
                self.applyNextMove()		
            
    def createNextMove(self,moveType):
        
        self.lastMoveType = moveType
        for i in range(0,4):
            self.blocks[i].nextPos.row = self.blocks[i].currentPos.row + directions[moveType][ROW]
            self.blocks[i].nextPos.col = self.blocks[i].currentPos.col + directions[moveType][COL]
            
    def movCollisionCheck_BLOCK(self,dirType,blockIndex):
        if dirType == 'down':
            if (self.blocks[blockIndex].currentPos.row+1 > self.rowNum-1) or self.blockMat[self.blocks[blockIndex].currentPos.row+directions[dirType][ROW]][self.blocks[blockIndex].currentPos.col+directions[dirType][COL]] != 'empty':
                return True
        else:
            if ( ((directions[dirType][COL])*(self.blocks[blockIndex].currentPos.col+directions[dirType][COL])) > ( ((self.colNum-1)+(directions[dirType][COL])*(self.colNum-1)) / 2 ) or 
                   self.blockMat[self.blocks[blockIndex].currentPos.row+directions[dirType][ROW]][self.blocks[blockIndex].currentPos.col+directions[dirType][COL]] != 'empty' ):
                return True
        return False	
            
    def movCollisionCheck(self,dirType): #Collision check for next move
        for i in range(0,4):
            if self.movCollisionCheck_BLOCK(dirType,i) == True:
                return True
        return False
        
    def rotCollisionCheck_BLOCK(self,blockCoor):
        if ( blockCoor[ROW]>self.rowNum-1 or blockCoor[ROW]<0 or blockCoor[COL]>self.colNum-1 or blockCoor[COL]<0 or self.blockMat[blockCoor[ROW]][blockCoor[COL]] != 'empty'):
            return True
        return False
        
    def rotCollisionCheck(self,blockCoorList): #Collision check for rotation
        for i in range(0,4):
            if self.rotCollisionCheck_BLOCK(blockCoorList[i]) == True:
                return True
        return False
        
    def spawnCollisionCheck(self,origin): #Collision check for spawn

        for i in range(0,4):
            spawnRow = origin[ROW] + pieceDefs[self.type][i][ROW]			
            spawnCol = origin[COL] + pieceDefs[self.type][i][COL]
            if spawnRow >= 0 and spawnCol >= 0:
                if self.blockMat[spawnRow][spawnCol] != 'empty':
                    return True
        return False
    
    def findOrigin(self):
        
        origin = [0,0]
        origin[ROW] = self.blocks[0].currentPos.row - self.currentDef[0][ROW]
        origin[COL] = self.blocks[0].currentPos.col - self.currentDef[0][COL]
        return origin
    
    def rotate(self):
        min = 3
        if self.type != 'O':
            tempBlocks = [[0] * 2 for i in range(4)]		
            origin = self.findOrigin()
            
            if self.type == 'I':
                pieceMatSize = 4
            else:
                pieceMatSize = 3
                
            for i in range(0,4):				
                tempBlocks[i][ROW] = origin[ROW] + self.currentDef[i][COL]
                tempBlocks[i][COL] = origin[COL] + (pieceMatSize - 1) - self.currentDef[i][ROW]
                                    
            if self.rotCollisionCheck(tempBlocks) == False:
                min = 100
                for i in range(0,4):
                    self.blocks[i].currentPos.row = tempBlocks[i][ROW]
                    self.blocks[i].currentPos.col = tempBlocks[i][COL]
                    self.currentDef[i][ROW] = self.blocks[i].currentPos.row - origin[ROW]
                    self.currentDef[i][COL] = self.blocks[i].currentPos.col - origin[COL]
                    if self.blocks[i].currentPos.col < min:
                        min = self.blocks[i].currentPos.col
        return min

    def spawn(self):

        self.dropScore = 0
        
        origin = [0,3]
        
        for i in range(0,4):		
            self.currentDef[i] = list(pieceDefs[self.type][i])	
        
        spawnTry = 0
        while spawnTry < 2:
            if self.spawnCollisionCheck(origin) == False:
                break
            else: 
                spawnTry = spawnTry + 1
                origin[ROW] = origin[ROW] - 1
                self.gameOverCondition = True
                self.status = 'collided'
                    
        for i in range(0,4):
            spawnRow = origin[ROW] + pieceDefs[self.type][i][ROW]			
            spawnCol = origin[COL] + pieceDefs[self.type][i][COL]
            self.blocks[i].currentPos.row = spawnRow
            self.blocks[i].currentPos.col = spawnCol
                
    def move(self,lastBlockMat,right,left):
        if self.status == 'uncreated':
            self.status = 'moving'
            self.blockMat = lastBlockMat			
            self.spawn()
            
        if self.status == 'moving':			
            if right:
                if self.movCollisionCheck('right') == True:
                    self.createNextMove('noMove')
                else:
                    self.createNextMove('right')
                    self.applyNextMove()				

            elif left:					
                if self.movCollisionCheck('left') == True:
                    self.createNextMove('noMove')
                else:
                    self.createNextMove('left')
                    self.applyNextMove()
                        
            else: # 'idle'
                if self.movCollisionCheck('down') == True:
                    self.createNextMove('noMove')
                    self.status = 'collided'
                else:
                    self.createNextMove('down')
                    self.slowMoveAction()
        
        else:
            pass

    def drop(self):
        gameClock.speedup()
        

# Class for the blocks of the moving piece. Each piece is made of 4 blocks in Tetris game		
class MovingBlock:

    def __init__(self):

        self.currentPos = self.CurrentPosClass(0,0)
        self.nextPos = self.NextPosClass(0,0)
    
    class CurrentPosClass:
    
        def __init__(self,row,col):
            self.row = row
            self.col = col
            
    class NextPosClass:
    
        def __init__(self,row,col):
            self.row = row
            self.col = col	
        
# Main game loop		
def gameLoop():		
    blockSize = 20 
    boardColNum = 10 
    boardRowNum = 20
    boardLineWidth = 10
    blockLineWidth = 1
    scoreBoardWidth = blockSize * (boardColNum//2)
    boardPosX = DISPLAY_WIDTH*0.3
    boardPosY = DISPLAY_HEIGHT*0.15

    mainBoard = MainBoard(blockSize,boardPosX,boardPosY,boardColNum,boardRowNum,boardLineWidth,blockLineWidth,scoreBoardWidth)
    
    gameExit = False
    ai = AiHandler()
    while not gameExit: #Stay in this loop unless the game is quit
        if mainBoard.isNewPiece():
            ai.clearVariableProgram()
            matrix = mainBoard.getMatrix()
            currentPiece = mainBoard.getCurrentPiece()
            ai.changeVariableProgram(matrix,currentPiece)
            ai.execute(mainBoard)
            mainBoard.setNewPiece()
        
        for event in pygame.event.get():
    #		if event.type == pygame.KEYDOWN: #Keyboard keys press events
    #			if event.key == pygame.K_LEFT:
    #				mainBoard.move(False,True,1)
    #			if event.key == pygame.K_RIGHT:
    #				mainBoard.move(True,False,1)
    #			if event.key == pygame.K_UP:
    #				mainBoard.rotate(1)
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        gameDisplay.fill(BLACK) #Whole screen is painted black in every iteration before any other drawings occur 
            
        mainBoard.gameAction() #Apply all the game actions here	
        mainBoard.draw() #Draw the new board after game the new game actions
        gameClock.update() #Increment the frame tick
        
        pygame.display.update() #Pygame display update		
        clock.tick(60) #Pygame clock tick function(60 fps)
    pygame.quit()
    sys.exit()

def makeTextObjs(text, font, color):
    surf = font.render(text, False, color)
    return surf, surf.get_rect()

def showTextScreen(text):
    loop = True
    image = pygame.image.load("tetris.jpg")
    screenUpdate = pygame.transform.scale(image, (800, 600))
    gameDisplay.blit(screenUpdate,(0,0))
    titleSurf, titleRect = makeTextObjs(text, fontTitle, WHITE)
    titleRect.center = (int(DISPLAY_WIDTH / 2)+230, int(DISPLAY_HEIGHT / 2)-220)
    gameDisplay.blit(titleSurf, titleRect)
    pressKeySurf, pressKeyRect = makeTextObjs('Press any key to play.', fontSB, WHITE)
    pressKeyRect.center = (int(DISPLAY_WIDTH / 2)-230, int(DISPLAY_HEIGHT / 2)-50)
    gameDisplay.blit(pressKeySurf,pressKeyRect)
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                #loop = False
                gameLoop()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

# Main program	
gameClock = GameClock()	
showTextScreen("TETRIS")