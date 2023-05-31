row(0..19).
col(0..9).

min_row(L):-Z=#min{X,Y:mat(X,Y,1)},L=Z-4.

matrix_not_empty:-mat(X,Y,1).

min_row(16):-not matrix_not_empty.

%#show piece/2.

piece(X,Y)|nopiece(X,Y):-mat(X,Y,0),X>=Z,min_row(Z).

:- #count{X,Y:piece(X,Y)} !=4.

rot(0)|rot(1)|rot(2)|rot(3).

%piece constraint


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
shape("j",2):-piece(X,Y),piece(X,Y+1),piece(X,Y+2), piece(X+1,Y+2).  
shape("j",3):-piece(X,Y),piece(X+1,Y),piece(X+2,Y),piece(X+2,Y-1).  

shape("l",0):-piece(X,Y), piece(X+1,Y), piece(X+1,Y-1), piece(X+1,Y-2).
shape("l",1):-piece(X,Y), piece(X+1,Y), piece(X+2,Y), piece(X+2,Y+1).
shape("l",2):-piece(X,Y),piece(X,Y+1),piece(X,Y+2), piece(X+1,Y).
shape("l",3):-piece(X,Y),piece(X,Y+1),piece(X+1,Y+1),piece(X+2,Y+1).





:-currentpiece(X),rot(Y),not shape(X,Y).

hole(X,Y):-mat(A,Y,1),mat(X,Y,0), min_row(L), A>=L, A<X.
hole(X,Y):-piece(A,Y),mat(X,Y,0), not piece(X,Y), min_row(L), A>=L, A<X.
:-hole(X,Y),piece(X,Y).


at_least_one_down:-piece(X,Y),mat(X+1,Y,1).
last_row:-piece(19,_).

:-not last_row, not at_least_one_down.

cambioStrategia:- min_row(L), L<=8.

clearedRow(X):-row(X),#count{Y:mat(X,Y,1)}=N,#count{Y:piece(X,Y)}=N2,N+N2=10.





%clear rows
:~ row(X),not clearedRow(X).[1@2, X]
%play as flat as possible,don t create excessive differences in column height
:~ piece(X,Y), not cambioStrategia. [19-X@1, X,Y]
%minimize holes
:~ hole(X,Y), not cambioStrategia. [X@3, X,Y]

:~row(X),not clearedRow(X).[1@3, X]
:~ piece(X,Y), cambioStrategia. [19-X@2, X,Y]
:~ hole(X,Y), cambioStrategia. [X@1, X,Y]



result(X,Y):-rot(Y),X=#min{J:piece(I,J)}.