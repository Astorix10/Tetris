from languages.predicate import Predicate

class Result(Predicate):
    predicate_name="result"

    def __init__(self,col=None,rotation=None):
        Predicate.__init__(self,[("col"),("rotation")])
        self.col = col
        self.rotation = rotation
        
    def get_col(self):
        return self.col
        
    def get_rotation(self):
        return self.rotation


    def set_col(self,col):
        self.col = col

   

    def set_rotation(self,rotation):
        self.rotation = rotation
        
    def __str__(self):
        return "result(" + str(self.col) + "," + str(self.rotation) +")"