import board

class Chess():
    
    """
    A class to represent the game of chess.
    
    ...

    Attributes:
    -----------
    board : Board
        represents the chess board of the game

    turn : bool
        True if white's turn

    white_ghost_piece : tup
        The coordinates of a white ghost piece representing a takeable pawn for en passant

    black_ghost_piece : tup
        The coordinates of a black ghost piece representing a takeable pawn for en passant

    Methods:
    --------
    promote(pos:stup) -> None
        Promotes a pawn that has reached the other side to another, or the same, piece

    move(start:tup, to:tup) -> None
        Moves the piece at `start` to `to` if possible. Otherwise, does nothing.
    """

    def __init__(self, initboard, myinit=True):
        
        if myinit:
            self.board = board.Board(initboard,False)
        else:
            self.board = board.Board([],True)
            
        self.turn = True

    def move(self, start, to, verbose=False):

        """
        Moves a piece at `start` to `to`. Does nothing if there is no piece at the starting point.
        Does nothing if the piece at `start` belongs to the wrong color for the current turn.
        Does nothing if moving the piece from `start` to `to` is not a valid move.

        start : tup
            Position of a piece to be moved

        to : tup
            Position of where the piece is to be moved
        
        precondition: `start` and `to` are valid positions on the board
        """

        if self.board.board[start[0]][start[1]] == None:
            if verbose:
                print("There is no piece to move at the start place")
            return

        target_piece = self.board.board[start[0]][start[1]]
        end_piece = self.board.board[to[0]][to[1]]
        is_end_piece = end_piece != None

        # Checks if a player's own piece is at the `to` coordinate
        if is_end_piece and self.board.board[start[0]][start[1]].color == end_piece.color:
            if verbose:
                print("There's a piece in the path.")
            return

        if target_piece.is_valid_move(self.board, start, to):
            # Special check for if the move is castling
            # Board reconfiguration is handled in Piece
            if target_piece.name == 'K' and abs(start[1] - to[1]) == 2:
                if verbose:
                    print("castled")
            
                if self.turn and self.black_ghost_piece:
                    self.board.board[self.black_ghost_piece[0]][self.black_ghost_piece[1]] = None
                elif not self.turn and self.white_ghost_piece:
                    self.board.board[self.white_ghost_piece[0]][self.white_ghost_piece[1]] = None
                self.turn = not self.turn
                return

            if self.board.board[to[0]][to[1]]:
                if verbose:
                    print(str(self.board.board[to[0]][to[1]]) + " taken.")
                # Special logic for ghost piece, deletes the actual pawn that is not in the `to`
                # coordinate from en passant
                if self.board.board[to[0]][to[1]].name == "GP":
                    if self.turn:
                        self.board.board[
                            self.black_ghost_piece[0] + 1
                        ][
                            self.black_ghost_piece[1]
                        ] = None
                        self.black_ghost_piece = None
                    else:
                        self.board.board[self.white_ghost_piece[0] - 1][self.black_ghost_piece[1]] = None
                        self.white_ghost_piece = None

                # Delete the taken piece from the current state
                if self.turn:
                    self.board.currentStateB = [x for x in self.board.currentStateB if [x[0],x[1]] != to]
                else:
                    self.board.currentStateW = [x for x in self.board.currentStateW if [x[0],x[1]] != to]

            self.board.board[to[0]][to[1]] = target_piece
            self.board.board[start[0]][start[1]] = None
            if verbose:
                print(str(target_piece) + " moved.")

            # AI state change - identify change to make in state
            if self.turn:
                for m in range(len(self.board.currentStateW)):
                    aa = self.board.currentStateW[m]               
                    # only the one to move
                    if self.board.listNames[int(aa[2]-1)] == target_piece.name and target_piece.color:
                        if verbose:
                            print("->piece initial state ",self.board.currentStateW[m])
                        self.board.currentStateW[m][0] = to[0]
                        self.board.currentStateW[m][1] = to[1]
                        if verbose:
                            print("->piece to state ",self.board.currentStateW[m])                                
            else:
                for m in range(len(self.board.currentStateB)):
                    aa = self.board.currentStateB[m]               
                    # only the one to move
                    if self.board.listNames[int(aa[2]-1)] == target_piece.name and not target_piece.color:
                        if verbose:
                            print("->piece initial state ",self.board.currentStateB[m])
                        self.board.currentStateB[m][0] = to[0]
                        self.board.currentStateB[m][1] = to[1]
                        if verbose:
                            print("->piece to state ",self.board.currentStateB[m])
        
            # alternate player
            self.turn = not self.turn
            
    def moveSim(self, start, to, verbose=False):

        """
        Moves a piece at `start` to `to`. Does nothing if there is no piece at the starting point.
        Does nothing if the piece at `start` belongs to the wrong color for the current turn.
        Does nothing if moving the piece from `start` to `to` is not a valid move.

        start : tup
            Position of a piece to be moved

        to : tup
            Position of where the piece is to be moved
        
        precondition: `start` and `to` are valid positions on the board
        """

        if self.board.board[start[0]][start[1]] == None:
            if verbose:
                print("There is no piece to move at the start place")
            return

        target_piece = self.board.board[start[0]][start[1]]
        end_piece = self.board.board[to[0]][to[1]]
        is_end_piece = end_piece != None

        # Checks if a player's own piece is at the `to` coordinate
        if is_end_piece and self.board.board[start[0]][start[1]].color == end_piece.color:
            if verbose:
                print("There's a piece in the path.")
            return

        if target_piece.is_valid_move(self.board, start, to):
            self.board.board[to[0]][to[1]] = target_piece
            self.board.board[start[0]][start[1]] = None
            if verbose:
                print(str(target_piece) + " moved.")

            # AI state change - identify change to make in state
            for m in range(len(self.board.currentStateW)):
                aa = self.board.currentStateW[m]               
                # only the one to move
                if self.board.listNames[int(aa[2]-1)] == target_piece.name and target_piece.color:
                    if verbose:
                        print("->piece initial state ",self.board.currentStateW[m])
                    self.board.currentStateW[m][0] = to[0]
                    self.board.currentStateW[m][1] = to[1]
                    if verbose:
                        print("->piece to state ", self.board.currentStateW[m])                 
                   
    def getListNextStatesSim(self):
        return self.board.getListNextStatesWSim()
    
    def getListNextStates(self):
        return self.board.getListNextStatesW() if self.turn else self.board.getListNextStatesB()  
