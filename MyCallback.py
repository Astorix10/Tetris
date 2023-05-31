from base.callback import Callback
from Result import Result
from CurrentPiece import CurrentPiece
from Mat import Mat

class MyCallback(Callback):
    def __init__(self,mainBoard):
        self.mainBoard = mainBoard
      
    def callback(self,answerSets):
        print("chiamata")
        for answerSet in answerSets.get_optimal_answer_sets():
                for ans in answerSet.get_atoms():
                      
                      if isinstance(ans,CurrentPiece):
                        print(ans.get_piece())
                      if isinstance(ans,Result):
                            minCol = self.mainBoard.rotate(int(ans.get_rotation()))

                            if self.mainBoard.getCurrentPiece() == "o":
                                minCol = 4

                            col = int(ans.get_col())
                            n = col - minCol

                            if n>0:
                                self.mainBoard.move(True,False,n)
                            elif n<0:
                                self.mainBoard.move(False,True,abs(n))
                      if  isinstance(ans,Mat):
                        print (ans)
        self.mainBoard.drop()
