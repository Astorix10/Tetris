row(0..19).
col(0..9).


min_row(L):-Z=#min{X,Y:mat(X,Y,1)},L=Z-4.

matrix_not_empty:-mat(X,Y,1).

min_row(16):-not matrix_not_empty.



piece(X,Y)|nopiece(X,Y):-mat(X,Y,0),X>=Z,min_row(Z).


%nextPiece(X,Y)|nonextPiece(X,Y):-mat(X,Y,0),X>=Z,min_row(Z).

%:-#count{X,Y:nextPiece(X,Y)}!=4.


:- #count{X,Y:piece(X,Y)} !=4.

rot(0)|rot(1)|rot(2)|rot(3).



shape("i",0):-piece(X,Y),piece(X,Y+1),piece(X,Y+2),piece(X,Y+3).
shape("i",1):-piece(X,Y),piece(X+1,Y),piece(X+2,Y),piece(X+3,Y).

shape("i",2):-shape("i",0).
shape("i",3):-shape("i",1).



shape("o",0):-piece(X,Y),piece(X,Y+1),piece(X+1,Y),piece(X+1,Y+1).
shape("o",Y):-shape("o",Z),Y=Z+1,Z<3.


shape("t",0):-piece(X,Y),piece(X+1,Y-1),piece(X+1,Y),piece(X+1,Y+1).
shape("t",1):-piece(X,Y),piece(X+1,Y),piece(X+2,Y),piece(X+1,Y+1).
shape("t",2):-piece(X,Y),piece(X,Y+1),piece(X,Y+2),piece(X+1,Y+1).
shape("t",3):-piece(X,Y),piece(X+1,Y),piece(X+2,Y),piece(X+1,Y-1).

shape("s",0):-piece(X,Y),piece(X,Y+1),piece(X+1,Y),piece(X+1,Y-1).
shape("s",1):-piece(X,Y),piece(X+1,Y),piece(X+1,Y+1),piece(X+2,Y+1).

shape("s",2):-shape("s",0).
shape("s",3):-shape("s",1).

shape("z",0):- piece(X,Y),piece(X,Y+1),piece(X+1,Y+1),piece(X+1,Y+2).
shape("z",1):- piece(X,Y),piece(X-1,Y),piece(X-1,Y+1),piece(X-2,Y+1).

shape("z",2):-shape("z",0).
shape("z",3):-shape("z",1).


shape("j",0):-piece(X,Y), piece(X+1,Y), piece(X+1,Y+1), piece(X+1,Y+2).
shape("j",1):-piece(X,Y), piece(X+1,Y), piece(X+2,Y), piece(X,Y+1).
shape("j",2):-piece(X,Y), piece(X,Y+1), piece(X,Y+2), piece(X+1,Y+2).  
shape("j",3):-piece(X,Y), piece(X+1,Y), piece(X+2,Y), piece(X+2,Y-1).  

shape("l",0):-piece(X,Y), piece(X+1,Y), piece(X+1,Y-1), piece(X+1,Y-2).
shape("l",1):-piece(X,Y), piece(X+1,Y), piece(X+2,Y), piece(X+2,Y+1).
shape("l",2):-piece(X,Y), piece(X,Y+1), piece(X,Y+2), piece(X+1,Y).
shape("l",3):-piece(X,Y), piece(X,Y+1), piece(X+1,Y+1), piece(X+2,Y+1).




%%%%%%%%%%%%

%nextshape("i",0):-nextPiece(X,Y),nextPiece(X,Y+1),nextPiece(X,Y+2),nextPiece(X,Y+3).
%nextshape("i",1):-nextPiece(X,Y),nextPiece4(X+1,Y),nextPiece4(X+2,Y),nextPiece(X+3,Y).

%nextshape("i",2):-nextshape("i",0).
%nextshape("i",3):-nextshape("i",1).



%nextshape("o",0):-nextPiece(X,Y),nextPiece(X,Y+1),nextPiece(X+1,Y),nextPiece(X+1,Y+1).
%nextshape("o",Y):-nextshape("o",Z),Y=Z+1,Z<3.


%nextshape("t",0):-nextPiece(X,Y),nextPiece(X+1,Y-1),nextPiece(X+1,Y),nextPiece(X+1,Y+1).
%nextshape("t",1):-nextPiece(X,Y),nextPiece(X+1,Y),nextPiece(X+2,Y),nextPiece(X+1,Y+1).
%nextshape("t",2):-nextPiece(X,Y),nextPiece(X,Y+1),nextPiece(X,Y+2),nextPiece(X+1,Y+1).
%nextshape("t",3):-nextPiece(X,Y),nextPiece(X+1,Y),nextPiece(X+2,Y),nextPiece(X+1,Y-1).

%nextshape("s",0):-nextPiece(X,Y),nextPiece(X,Y+1),nextPiece(X+1,Y),nextPiece(X+1,Y-1).
%nextshape("s",1):-nextPiece(X,Y),nextPiece(X+1,Y),nextPiece(X+1,Y+1),nextPiece(X+2,Y+1).

%nextshape("s",2):-nextshape("s",0).
%nextshape("s",3):-nextshape("s",1).

%nextshape("z",0):- nextPiece(X,Y),nextPiece(X,Y+1),nextPiece(X+1,Y+1),nextPiece(X+1,Y+2).
%nextshape("z",1):- nextPiece(X,Y),nextPiece(X-1,Y),nextPiece(X-1,Y+1),nextPiece(X-2,Y+1).

%nextshape("z",2):-nextshape("z",0).
%nextshape("z",3):-nextshape("z",1).


%nextshape("j",0):-nextPiece(X,Y), nextPiece(X+1,Y), nextPiece(X+1,Y+1), nextPiece(X+1,Y+2).
%nextshape("j",1):-nextPiece(X,Y), nextPiece(X+1,Y), nextPiece(X+2,Y), nextPiece(X,Y+1).
%nextshape("j",2):-nextPiece(X,Y), nextPiece(X,Y+1), nextPiece(X,Y+2), nextPiece(X+1,Y+2).  
%nextshape("j",3):-nextPiece(X,Y), nextPiece(X+1,Y), nextPiece(X+2,Y), nextPiece(X+2,Y-1).  

%nextshape("l",0):-nextPiece(X,Y), nextPiece(X+1,Y), nextPiece(X+1,Y-1), nextPiece(X+1,Y-2).
%nextshape("l",1):-nextPiece(X,Y), nextPiece(X+1,Y), nextPiece(X+2,Y), nextPiece(X+2,Y+1).
%nextshape("l",2):-nextPiece(X,Y), nextPiece(X,Y+1), nextPiece(X,Y+2), nextPiece(X+1,Y).
%nextshape("l",3):-nextPiece(X,Y), nextPiece(X,Y+1), nextPiece(X+1,Y+1), nextPiece(X+2,Y+1).
%%%

%%%%%
%:-nextpiece(X),nextrot(Y),not nextshape(X,Y).



%%%%%
%hole(X,Y):-nextPiece(A,Y),mat(X,Y,0), not piece(X,Y), min_row(L), A>=L, A<X.
%:-hole(X,Y),nextPiece(X,Y).
%%%%%



%at_least_one_down_next:-nextPiece(X,Y),mat(X+1,Y,1).
%last_row_next:-nextPiece(19,_).
%:-not last_row_next, not at_least_one_down_next.

:-currentpiece(X),rot(Y),not shape(X,Y).

at_least_one_down:-piece(X,Y),mat(X+1,Y,1).
last_row:-piece(19,_).

:-not last_row, not at_least_one_down.

hole(X,Y):-mat(A,Y,1),mat(X,Y,0), min_row(L), A>=L, A<X.
hole(X,Y):-piece(A,Y),mat(X,Y,0), not piece(X,Y), min_row(L), A>=L, A<X.
:-hole(X,Y),piece(X,Y).



cambioStrategia:- min_row(L), L<=9.



clearedRow(X):-row(X),#count{Y:mat(X,Y,1)}=N,#count{Y:piece(X,Y)}=N2,N+N2=10.

clearedRows(N):-N=#count{X:clearedRow(X)}.


%play as most as possible to the left
:~ piece(X,Y). [Y@1, X,Y]

%make tetris
:~ clearedRows(N),N<4,not cambioStrategia. [1@2, N]
%minimize holes
:~ hole(X,Y), not cambioStrategia. [20-X@5, X,Y]
%play as flat as possible,don t create excessive differences in column height
:~ piece(X,Y), not cambioStrategia. [19-X@3, X,Y]
%leave space for last column if not clearing row
:~ piece(X,Y), Y=9, clearedRows(N), N<1, not cambioStrategia. [1@4, X,Y]


:~ hole(X,Y),  cambioStrategia. [20-X@3, X,Y]
%clear rows
:~ row(X),not clearedRow(X),cambioStrategia.[1@2, X]
:~ piece(X,Y), cambioStrategia. [19-X@3, X,Y]



result(X,Y):-rot(Y),X=#min{J:piece(I,J)}.