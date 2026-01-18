"""
This class is responsible for storing all the information about
current state of the chess game.
It will also be responsible for determining valid moves at the
current state. It will also keep a move log.
"""

class GameState:    # I draw a chess board
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]

        # Movefunction to move all the pieces in right way and in right position
        self.moveFunctions = {
            'p': self.getPawnMoves, 'R': self.getRookMoves,
            'N': self.getKnightMoves, 'B': self.getBishopMoves,
            'Q': self.getQueenMoves, 'K': self.getKingMoves
        }


        # First turn white

        self.whiteToMoves = True
        self.movelog = []


    #Moves will be valid in only empty space

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.movelog.append(move)
        self.whiteToMoves = not self.whiteToMoves


    # if wrong Move is Placed then We should back it up So i introduced UNDO move by pressing key (Z)..

    def undoMove(self):
        if len(self.movelog) != 0:
            move = self.movelog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMoves = not self.whiteToMoves


    #Valid moves ko check kre ga ki age ki space khali h k nhi

    def getValidMoves(self):
        return self.getAllposibleMoves



    # sabhi posible moves dekhe ga on empty space or unhe moves m store kra de ga

    @property
    def getAllposibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if ((turn == 'w' and self.whiteToMoves) or
                    (turn == 'b' and not self.whiteToMoves)):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves



    # it checks how pawn will move first move can be 1 or can 2 sq_box..so it checks the move and as we know pawn cuts the enemy piece diagonally so it will check this also
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMoves:
            if self.board[r - 1][c] == "--":
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0 and self.board[r - 1][c - 1][0] == "b":
                moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 <= 7 and self.board[r - 1][c + 1][0] == "b":
                moves.append(Move((r, c), (r - 1, c + 1), self.board))
        else:
            if self.board[r + 1][c] == "--":
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0 and self.board[r + 1][c - 1][0] == "w":
                moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7 and self.board[r + 1][c + 1][0] == "w":
                moves.append(Move((r, c), (r + 1, c + 1), self.board))


    # Rook moves in empty space until enemy piece interpt or it own side piece...
    # Rook move only forward, Backward, Right and Left..not diagonally..
    #if Enemy piece interpt then it cuts down it and store that in moves list

    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMoves else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break


    # Knight moves 2.5 moves two step forward or backward or right or in left but after two step it move 1 perpendicular
    # if it moves forward or backward its perpendicular is right and left and if it moves left or right its perpendicular is froward and backward

    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2),
                       (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMoves else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    #Bishop moves diagonally on its path if its black it moves diagonally only on black and same as white
    #Untill Enemy piece interpt or it own side piece

    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = "b" if self.whiteToMoves else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    #Queen moves in each direction freely until Enemy piece interpt or it own side piece.
    #Queen moves  is a combination of Bishop moves and Rook moves..

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)


    #king can only move 1 block of square in each direction

    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1, -1), (-1, 0), (-1, 1),
                     (0, -1), (0, 1),
                     (1, -1), (1, 0), (1, 1))
        allyColor = "w" if self.whiteToMoves else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))



    #getCountKings this function checks if there is only one king left on board or not
    # if it two king left then the game will continue otherwise it show check-mate

    def getCountKings(self):
        return sum(
            1 for r in range(len(self.board))
            for c in range(len(self.board[r]))
            if self.board[r][c] in ("wK", "bK")
        )


#Class moves  firstly we give each block it own identity
#like a1 or b3 just like that

#class move calculate the move and store the value which is moved by the user is it pawn, is it Rook, or is it another piece which is available on board
#it prints the identity of the move from it start to where it end.

class Move:
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, stSquare, endSquare, board):
        self.startRow = stSquare[0]
        self.startCol = stSquare[1]
        self.endRow = endSquare[0]
        self.endCol = endSquare[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol


    # this function gives return id of the piece to where it moved

    def __eq__(self, other):
        return isinstance(other, Move) and self.moveID == other.moveID

    #it checks the notation of the chess game

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    #it ranks the file or we can say it generate the dictionary of the moves key and value of the key

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
