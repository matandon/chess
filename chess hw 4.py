import copy

#################################################
# Chess Functions
#################################################

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
    Moves = [(newRow,startCol-1),(newRow,startCol+1)]
    forwardMove = (newRow,startCol)
    if board[forwardMove[0]][forwardMove[1]] == " ":
        validMoves += [forwardMove]
    for move in Moves:
        if not (move[1] < 0 or move[1] > len(board[0])):
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
                break
            else:
                break
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

def testGetValidPawnMoves():
    print("Testing getValidPawnMoves()...", end="")
    # TODO fill in the board such that the test case passes!
    board = [
        ['♟', '♙', '♟'],
        [' ', '♙', ' '],
        ['♙', ' ', '♙'],
    ]
    assert(getValidPawnMoves(board, 0, 1) == [])
    assert(sorted(getValidPawnMoves(board, 0, 0)) == [(1, 0), (1, 1)])
    assert(sorted(getValidPawnMoves(board, 1, 1)) == [(0, 0), (0, 2)])
    print("Passed!")


def testGetValidRookMoves():
    print("Testing getValidRookMoves()...", end="")
    # TODO fill in the board such that the test case passes!
    board = [
        [' ', ' ', ' '],
        [' ', ' ', ' '],
        [' ', '♖', '♖'],
        [' ', ' ', ' '],
    ]
    assert(sorted(getValidRookMoves(board, 2, 1)) == [(0, 1), (1, 1), (2, 0),
                                                      (3, 1)])
    print("Passed!")


def testGetValidBishopMoves():
    print("Testing getValidBishopMoves()...", end="")
    # TODO fill in the board such that the test case passes!
    board = [
        [' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' '],
        [' ', '♗', ' ', ' '],
        [' ', ' ', '♗', ' '],
    ]
    assert(sorted(getValidBishopMoves(board, 2, 1)) == [(0, 3),
                                                        (1, 0), (1, 2),
                                                        (3, 0)])
    print("Passed!")


def testGetValidQueenMoves():
    print("Testing getValidQueenMoves()...", end="")
    # TODO fill in the board such that the test case passes!
    board = [
        [' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' '],
        [' ', '♕', ' ', ' '],
        [' ', ' ', '♕', ' '],
    ]
    assert(sorted(getValidQueenMoves(board, 2, 1)) == [(0, 1), (0, 3),
                                                       (1, 0), (1, 1), (1, 2),
                                                       (2, 0), (2, 2), (2, 3),
                                                       (3, 0), (3, 1)])
    print("Passed!")


def testGetValidKnightMoves():
    print("Testing getValidKnightMoves()...", end="")
    # TODO fill in the board such that the test case passes!
    board = [
        [' ', ' ', '♘', ' '],
        [' ', ' ', ' ', ' '],
        [' ', '♘', ' ', ' '],
        [' ', ' ', ' ', ' '],
    ]
    assert(sorted(getValidKnightMoves(board, 2, 1)) == [(0, 0), (1, 3), (3, 3)])
    print("Passed!")


def testGetValidKingMoves():
    print("Testing getValidKingMoves()...", end="")
    # TODO fill in the board such that the test case passes!
    board = [
        [' ', ' ', ' '],
        [' ', '♔', ' '],
        [' ', ' ', '♔'],
    ]
    assert(sorted(getValidKingMoves(board, 1, 1)) == [(0, 0), (0, 1), (0, 2),
                                                      (1, 0), (1, 2),
                                                      (2, 0), (2, 1)])
    print("Passed!")


def testGetValidChessMoves():
    testGetValidPawnMoves()
    testGetValidRookMoves()
    testGetValidBishopMoves()
    testGetValidQueenMoves()
    testGetValidKingMoves()
    testGetValidKnightMoves()
    print("Testing getValidChessMoves()...", end="")
    # sanity check
    board = [
        ['♟', '♟', '♟'],
        [' ', '♔', ' '],
        [' ', ' ', '♙'],
    ]
    assert(getValidChessMoves(board, 0, 0) == getValidPawnMoves(board, 0, 0))
    assert(getValidChessMoves(board, 1, 1) == getValidKingMoves(board, 1, 1))
    assert(getValidChessMoves(board, 1, 0) == None) # TODO
    print("Passed!")

def testAll():
    testGetValidChessMoves()


def main():
    testAll()


if __name__ == '__main__':
    main()
