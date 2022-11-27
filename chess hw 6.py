#################################################
# hw6.py
#
# Your name:
# Your andrew id:
# Collaborators:
# (collaborators = comma separated andrew ids)
#################################################

import copy
import decimal

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

######################################################################
# Your Functions and OOP class definitions
######################################################################

def getValidPawnMoves(board, startRow, startCol):
    piece = board[startRow][startCol]
    pieceName, color = getPieceInfo(piece)
    validMoves = []
    if color == "black":
        newRow = startRow + 1
    elif color == "white":
        newRow = startRow - 1
    if newRow < 0 or newRow > len(board):
        return validMoves
    diagMoves = [(newRow,startCol-1),(newRow, startCol+1)]
    forwardMove = (newRow,startCol)
    if board[forwardMove[0]][forwardMove[1]] == " ":
        validMoves += [forwardMove]
    for move in diagMoves:
        if (move[1] >= 0 and move[1] < len(board[0])):
            pieceAtPos = board[move[0]][move[1]]
            if getPieceInfo(pieceAtPos)[1] != color:
                validMoves += [move]
    return validMoves


def isSpace(board, row, col):
    if board[row][col] == " ":
        return True
    return False


def getValidRookMoves(board, startRow, startCol):
    validMoves = []
    color = getPieceInfo(board[startRow][startCol])[1]
    for upRow in range(startRow - 1, -1, -1):
        if isSpace(board, upRow, startCol):
            validMoves += [(upRow, startCol)]
        else:
            if getPieceInfo(board[upRow][startCol])[1] != color:
                validMoves += [(upRow, startCol)]
            break
    for downRow in range(startRow + 1, len(board)):
        if isSpace(board, downRow, startCol):
            validMoves += [(downRow, startCol)]
        else:
            if getPieceInfo(board[downRow][startCol])[1] != color:
                validMoves += [(downRow, startCol)]
            break
    for leftCol in range(startCol - 1, -1, -1):
        if isSpace(board, startRow, leftCol):
            validMoves += [(startRow, leftCol)]
        else:
            if getPieceInfo(board[startRow][leftCol])[1] != color:
                validMoves += [(startRow, leftCol)]
            break
    for rightCol in range(startCol + 1, len(board[0])):
        if isSpace(board, startRow, rightCol):
            validMoves += [(startRow, rightCol)]
        else:
            if getPieceInfo(board[startRow][rightCol])[1] != color:
                validMoves += [(startRow, rightCol)]
            break
    return validMoves


def inBounds(board, row, col):
    if row >= 0 and row < len(board) and col >= 0 and col < len(board[0]):
        return True
    return False


def extendInDirection(board, startRow, startCol, dRow, dCol):
    curRow, curCol = startRow + dRow, startCol + dCol
    moves = []
    pieceColor = getPieceInfo(board[startRow][startCol])[1]
    while inBounds(board,curRow,curCol):
        if isSpace(board, curRow, curCol):
            moves += [(curRow, curCol)]
        elif getPieceInfo(board[curRow][curCol])[1] != pieceColor:
            moves += [(curRow, curCol)]
            break
        else:
            break
        curRow += dRow
        curCol += dCol
    return moves


def getValidBishopMoves(board, startRow, startCol):
    directions = [(-1,-1),(1,1),(-1,1),(1,-1)]
    validMoves = []
    for drow,dcol in directions:
        validMoves.extend(extendInDirection(board,startRow,startCol,drow,dcol))
    return validMoves


def getValidQueenMoves(board, startRow, startCol):
    vertMoves = getValidBishopMoves(board, startRow, startCol)
    diagMoves = getValidRookMoves(board, startRow, startCol)
    validMoves = vertMoves + diagMoves
    return validMoves


def getValidKnightMoves(board, startRow, startCol):
    values = [(2, 1), (2, -1), (-2, -1), (-2, 1), (1, 2), (-1, 2), (1, -2), 
              (-1, -2)]
    validMoves = []
    for drow, dcol in values:
        validMoves.extend(extendInDirection(board,startRow,startCol,drow,dcol))
    return validMoves


def getValidKingMoves(board, startRow, startCol):
    validMoves = []
    color = getPieceInfo(board[startRow][startCol])[1]
    directions = [ (-1, -1), (-1, 0), (-1, +1),
                   ( 0, -1),          ( 0, +1),
                   (+1, -1), (+1, 0), (+1, +1)]
    for drow, dcol in directions:
        newRow, newCol = startRow + drow, startCol + dcol
        if inBounds(board, newRow, newCol):
            if isSpace(board, newRow, newCol):
                validMoves += [(newRow, newCol)]
            elif getPieceInfo(board[newRow][newCol])[1] != color:
                validMoves += [(newRow, newCol)]
    return validMoves

def getValidChessMoves(board, row, col):
    # for your reference
    whitePieces = '♖♘♗♕♔♙'
    blackPieces = '♜♞♝♛♚♟'
    if board[row][col] != " ":
        piece, color = getPieceInfo(board[row][col])
        if piece == "pawn":
            return getValidPawnMoves(board, row, col)
        elif piece == "rook":
            return getValidRookMoves(board, row, col)
        elif piece == "bishop":
            return getValidBishopMoves(board, row, col)
        elif piece == "queen":
            return getValidQueenMoves(board, row, col)
        elif piece == "king":
            return getValidKingMoves(board, row, col)
        elif piece == "knight":
            return getValidKnightMoves(board, row, col)
    else:
        return None

def getPieceInfo(piece):
    whitePieces = '♖♘♗♕♔♙'
    blackPieces = '♜♞♝♛♚♟'
    pieces = ["rook","knight","bishop","queen","king","pawn"]
    if piece in whitePieces:
        return (pieces[whitePieces.find(piece)],"white")
    elif piece in blackPieces:
        return (pieces[blackPieces.find(piece)],"black")

class ChessGame(object):
    def __init__(self, board):
        self.board = board
        self.turn = "white"
        self.whiteTaken = []
        self.blackTaken = []
        self.moves = []
        self.undoMoves = []

    def getBoard(self):
        return self.board
    
    def getWhiteTaken(self):
        return self.whiteTaken

    def getBlackTaken(self):
        return self.blackTaken
    
    def getTurn(self):
        return self.turn
    
    def isValidMove(self, fromRow, fromCol, toRow, toCol):
        validMovesList = getValidChessMoves(self.board, fromRow, fromCol)
        if (toRow, toCol) in validMovesList:
            return True
        return False
    
    def switchTurns(self):
        if self.turn == "black":
            self.turn = "white"
        else:
            self.turn = "black"

    def makeMove(self, fromRow, fromCol, toRow, toCol):
        piece = self.board[toRow][toCol]
        if self.isValidMove(fromRow, fromCol, toRow, toCol):
            if piece != " ":
                if self.turn == "black":
                    self.whiteTaken += [self.board[toRow][toCol]]
                else:
                    self.blackTaken += [self.board[toRow][toCol]]
            self.board[toRow][toCol] = self.board[fromRow][fromCol]
            self.board[fromRow][fromCol] = " "
            self.switchTurns()
            self.moves += [(fromRow, fromCol, toRow, toCol, piece)]
            self.undoMoves = []
            return True
        return False

    def undoMove(self):
        if self.moves != []:
            ogRow, ogCol, curRow, curCol, piece = self.moves.pop()
            self.board[ogRow][ogCol] = self.board[curRow][curCol]
            self.board[curRow][curCol] = piece
            self.undoMoves += [(curRow, curCol, ogRow, ogCol, piece)]
            self.switchTurns()
            if piece != " ":
                if getPieceInfo(piece)[1] == "black":
                    self.blackTaken.pop()
                else:
                    self.whiteTaken.pop()
            return True
        return False
    
    def redoMove(self):
        if self.undoMoves != []:
            toRow, toCol, fromRow, fromCol, piece = self.undoMoves.pop()
            self.board[toRow][toCol] = self.board[fromRow][fromCol]
            self.board[fromRow][fromCol] = " "
            self.moves += [(fromRow, fromCol, toRow, toCol, piece)]
            self.switchTurns()
            if piece != " ":
                if getPieceInfo(piece)[1] == "black":
                    self.blackTaken.append(piece)
                else:
                    self.whiteTaken.append(piece)
            return True
        return False

    def checkGameOver(self):
        if "♔" in self.whiteTaken:
            return True, "black"
        elif "♚" in self.blackTaken:
            return True, "white"
        else:
            return False, "none"

#################################################################
# Test Functions
#################################################################

def testChessGame():
    print("testing chessGame...", end="")
    board = [
        ['♟', '♚', '♟'],
        [' ', '♔', ' '],
        [' ', ' ', '♙'],
    ]
    initialBoard = copy.deepcopy(board)
    game = ChessGame(board)
    game.switchTurns()
    assert(game.getTurn() == "black")
    assert(game.getWhiteTaken() == game.getBlackTaken() == [])
    assert(game.checkGameOver() == (False, 'none'))

    # make two moves
    assert(game.makeMove(0, 0, 1, 0) == True)
    assert(game.getTurn() == "white")

    assert(game.makeMove(2, 2, 1, 2) == True)
    assert(game.getBoard() == [
        [' ', '♚', '♟'],
        ['♟', '♔', '♙'],
        [' ', ' ', ' '],
    ])

    # undo two moves. should switch turns
    assert(game.undoMove() == True)
    assert(game.getTurn() == "white")

    assert(game.undoMove() == True)
    assert(game.getTurn() == "black")
    assert(game.getBoard() == initialBoard)

    # redo the move
    assert(game.redoMove() == True)
    assert(game.getTurn() == "white")
    assert(game.getBoard() == [
        [' ', '♚', '♟'],
        ['♟', '♔', ' '],
        [' ', ' ', '♙'],
    ])
    assert(game.makeMove(1, 1, 0, 2) == True)
    assert(game.getBlackTaken() == ['♟'])
    assert(game.getBoard() == [
        [' ', '♚', '♔'],
        ['♟', ' ', ' '],
        [' ', ' ', '♙'],
    ])
    # can't redo a move since we made a new move
    assert(game.redoMove() == False)

    # undoing a move should undo taken pieces too
    assert(game.undoMove() == True)
    assert(game.getBoard() == [
        [' ', '♚', '♟'],
        ['♟', '♔', ' '],
        [' ', ' ', '♙'],
    ])
    assert(game.getBlackTaken() == [])

    # we can still undo moves after we placed a move that overrides redo's
    assert(game.undoMove() == True)
    assert(game.redoMove() == True)

    # redo the move and the piece should be taken now
    assert(game.redoMove() == True)
    assert(game.getBlackTaken() == ['♟'])

    # take the king
    assert(game.makeMove(0, 1, 0, 2) == True)
    assert(game.getBoard() == [
        [' ', ' ', '♚'],
        ['♟', ' ', ' '],
        [' ', ' ', '♙'],
    ])
    assert(game.checkGameOver() == (True, "black"))
    print("passed!")


#################################################
# testAll and main
#################################################

def testAll():
    testChessGame()

def main():
    testAll()

if __name__ == "__main__":
    main()