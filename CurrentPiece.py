from languages.predicate import Predicate
from specializations.dlv2.desktop.dlv2_desktop_service import DLV2DesktopService
from platforms.desktop.desktop_handler import DesktopHandler
from languages.asp.asp_input_program import ASPInputProgram
from languages.asp.asp_mapper import ASPMapper
from base.callback import Callback
class CurrentPiece(Predicate):
    predicate_name="currentpiece"

    def __init__(self,piece=None):
        Predicate.__init__(self,[("piece")])
        self.piece = piece
        
    def get_piece(self):
        return self.piece
        
    def set_piece(self, piece):
        self.piece = piece
        
    def __str__(self):
        return "currentpiece(" + self.piece + ")"