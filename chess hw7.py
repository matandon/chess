#################################################
# hw7.py
#
# Your Name:
# Your Andrew ID:
# Collaborators:
# (collaborators = comma separated andrew ids)
#################################################

from cmu_112_graphics import App
import copy

####################################
# Add your hw4, hw5 and hw6 functions here!
# You may need to modify them a bit.
####################################

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
        if (move[1] >= 0 and move[1] < len(board[0])) and board[move[0]][move[1]] != " ":
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
    pieceColor = getPieceInfo(board[startRow][startCol])[1]
    for drow, dcol in values:
        curRow, curCol = startRow + drow, startCol + dcol
        if inBounds(board, curRow, curCol):
            if isSpace(board, curRow, curCol):
                validMoves += [(curRow, curCol)]
            elif getPieceInfo(board[curRow][curCol])[1] != pieceColor:
                validMoves += [(curRow, curCol)]
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
            return True, "Black"
        elif "♚" in self.blackTaken:
            return True, "White"
        else:
            return False, "none"

def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

def drawChessBoard(canvas, width, height, board, color, margin, moves, curPos):
    rows = len(board)
    cols = len(board[0])
    cellWidth = (width-2*margin)/cols
    cellHeight = (height-2*margin)/rows
    r, g, b = color
    marginColor = rgbString(r,g,b)
    cellColor = rgbString(min(r+150,255),min(g+150,255),min(b+150,255))
    canvas.create_rectangle(0,0,width,height,fill=marginColor)
    fontSize = int((20/38)*cellHeight)
    for i in range(rows):
        for j in range(cols):
            fillColor = "white"
            width = 0 
            x1, y1 = (j*cellWidth) + margin, (i*cellHeight) + margin
            x2, y2 = x1+cellWidth, y1+cellHeight
            if (i+j)%2 == 1: 
                fillColor = cellColor
            if (i, j) in moves:
                width = 5
            if (i,j) == curPos:
                fillColor = "yellow"
            canvas.create_rectangle(x1,y1,x2,y2,width=width, outline = marginColor,fill=fillColor, tag = f"board[{i}][{j}]")  
            canvas.create_text((x1+x2)//2, (y1+y2)//2, text=board[i][j], font=f"Arial {fontSize}")

####################################
# Chess App!
####################################

class PlayChess(App):
    def appStarted(self, board):
        self.game = ChessGame(board)
        self.ogBoard = copy.deepcopy(board)
        self.rows = len(board)
        self.cols = len(board[0])
        self.margin = 30
        self.row = 0
        self.col = 0
        self.time = 20
        self.marginColor = (0,112,255)
        self.pieceSelected = False
        self.piece = ""
        self.validMoves = []
        self.oldCoord = []
        self.gameOver = False, "none"
        self.cellHeight = (self.height - 2*self.margin) // self.rows
        self.cellWidth = (self.width - 2*self.margin) // self.cols
        self.count = 0
        # TODO: more data initialization

    def makeMove(self):
        if (not self.pieceSelected) and self.game.board[self.row][self.col] != " ":
            self.piece = self.game.board[self.row][self.col]
            if getPieceInfo(self.piece)[1] == self.game.turn:
                self.pieceSelected = True
                self.validMoves = copy.deepcopy(getValidChessMoves(self.game.board, self.row, self.col))
                self.oldCoord = (self.row, self.col)
        elif self.pieceSelected:
            if (self.row, self.col) in self.validMoves:
                movingToPiece = self.game.board[self.row][self.col]
                if movingToPiece != " " and getPieceInfo(movingToPiece)[1] != self.game.turn:
                    if getPieceInfo(movingToPiece)[1] == "white":
                        self.game.whiteTaken += [movingToPiece]
                    elif getPieceInfo(movingToPiece)[1] == "black":
                        self.game.blackTaken += [movingToPiece]
                self.game.board[self.row][self.col] = self.piece
                self.game.board[self.oldCoord[0]][self.oldCoord[1]] = " "
                self.game.switchTurns()
                self.time = 20
                self.validMoves = []
                self.game.moves += [(self.oldCoord[0], self.oldCoord[1], self.row, self.col, movingToPiece)]
            self.pieceSelected = False
            self.piece = ""
            self.gameOver = self.game.checkGameOver()

    def keyPressed(self, event):
        # use event.key
        if not self.gameOver[0]:
            if event.key == "Down":
                self.row = (self.row + 1) % len(self.game.board)
            elif event.key == "Up":
                self.row = (self.row - 1) % len(self.game.board)
            elif event.key == "Left":
                self.col = (self.col - 1) % len(self.game.board)
            elif event.key == "Right":
                self.col = (self.col + 1) % len(self.game.board)
            elif event.key == "Space":
                self.makeMove()
            elif event.key == "r":
                self.game.redoMove()
            elif event.key == "u":
                self.game.undoMove()
        else:
            if event.key == "r":
                self.appStarted(self.ogBoard)
        
    def getState(self):
        return (self.game.board, self.game.blackTaken, self.game.whiteTaken, self.game.turn, self.time)

    def mousePressed(self, event):
        # use event.x and event.y
        if not self.gameOver[0]:
            if (event.x >= self.margin and event.x < self.width - 2*self.margin and
                event.y >= self.margin and event.y < self.width - 2*self.margin):
                self.row = int((event.y - self.margin) // self.cellHeight)
                self.col = int((event.x - self.margin) // self.cellWidth)
                self.makeMove()

    def timerFired(self):
        self.count += 1
        if self.count == 10:
            self.count = 0
            if self.time > 0:
                self.time -= 1
            
    def redrawAll(self, canvas):
        # TODO: draw board
        if not self.gameOver[0]:
            drawChessBoard(canvas, self.width, self.height, self.game.board, self.marginColor, self.margin, self.validMoves, (self.row, self.col))
            canvas.create_text(self.width//2, self.margin//2, text = f"{self.game.turn}'s turn", fill = "white", font = "Arial 15 bold")
            canvas.create_text(self.width//2, self.height - self.margin//2, text = f"{self.time}", font = "Arial 15 bold", fill = "white")
            offset = 20
            for i in range(len(self.game.blackTaken)):
                piece = self.game.blackTaken[i]
                canvas.create_text(self.margin//2, i*30 + self.height//2, text = piece, font = f"Arial {self.margin - 5}")
            for i in range(len(self.game.whiteTaken)):
                piece = self.game.whiteTaken[i]
                canvas.create_text(self.width - (self.margin//2), i*30 + self.height//2, text = piece, font = f"Arial {self.margin - 5}")
        else:
            canvas.create_rectangle(0, self.height//3, self.width, self.height//3 * 2, fill = "dark blue")
            canvas.create_text(self.width//2, self.height//2, text = f"{self.gameOver[1]} Won! Press r to restart.", fill = "white", font = "Arial 26 bold")
        # TODO: draw other parts of your animation too!

####################################
# Animation Tests!
####################################

def testChessKeyPressed():
    print("testing keypressed", end="...")
    initialBoard = [
        ['♟', '♚', '♟'],
        [' ', '♔', ' '],
        [' ', ' ', '♙'],
    ]
    app = PlayChess(copy.deepcopy(initialBoard), isTest=True)
    (board, blackTaken, whiteTaken, turn, time) = app.getState()
    assert(board == initialBoard)
    assert(blackTaken == whiteTaken == [])
    assert(turn == "white")

    # testing wraparound for keypresses: this should
    # result in (0, 0) still being the highlighted cell
    for key in ["Up", "Down", "Left", "Right"]:
        app.simulateKeyPress(key)
    for i in range(len(board)**2):
        app.simulateKeyPress("Right")

    # try to move a black pawn down, but fail because it isn't the correct turn
    # we're currently at (0, 0)
    app.simulateKeyPress("Space") # select the pawn
    app.simulateKeyPress("Down")
    app.simulateKeyPress("Space") # try to move it into place
    (board, blackTaken, whiteTaken, turn, time) = app.getState()
    assert(board == initialBoard)

    # go back and select + unselect the pawn
    # we're currently at (1, 0)
    app.simulateKeyPress("Up")
    app.simulateKeyPress("Space")
    app.simulateKeyPress("Space")
    # then go back and select a legal (white) piece to move
    # we're currently at (0, 0)
    app.simulateKeyPress("Down")
    app.simulateKeyPress("Right")
    app.simulateKeyPress("Space")
    # take the pawn with the king
    # we're currently at (1, 1)
    app.simulateKeyPress("Up")
    app.simulateKeyPress("Right")
    app.simulateKeyPress("Space")
    (board, blackTaken, whiteTaken, turn, time) = app.getState()
    assert(board == [
        ['♟', '♚', '♔'],
        [' ', ' ', ' '],
        [' ', ' ', '♙'],
    ])
    assert(blackTaken == ['♟'])
    assert(whiteTaken == [])
    assert(turn == "black")

    # # let's try undo and redo: undo should completely undo the move
    # # and redo should completely redo it!

    # let's end the game, and then press r to restart
    # we're currently at (0, 2)
    app.simulateKeyPress("Left")
    app.simulateKeyPress("Space")
    app.simulateKeyPress("Right")
    app.simulateKeyPress("Space")

    # now the game is over
    (board, blackTaken, whiteTaken, turn, time) = app.getState()
    assert(board == [
        ['♟', ' ', '♚'],
        [' ', ' ', ' '],
        [' ', ' ', '♙'],
    ])
    assert(blackTaken == ['♟'])
    assert(whiteTaken == ['♔'])

    # we press r to restart
    app.simulateKeyPress("r")
    (board, blackTaken, whiteTaken, turn, time) = app.getState()
    assert(board == initialBoard)
    assert(blackTaken == whiteTaken == [])
    assert(turn == "white")

    # for sanity, let's try making a move again.
    # then go back and select a legal (white) piece to move
    # we're currently at (0, 0)
    app.simulateKeyPress("Down")
    app.simulateKeyPress("Right")
    app.simulateKeyPress("Space")

    # take the pawn with the king
    # we're currently at (1, 1)
    app.simulateKeyPress("Up")
    app.simulateKeyPress("Right")
    app.simulateKeyPress("Space")
    (board, blackTaken, whiteTaken, turn, time) = app.getState()
    assert(board == [
        ['♟', '♚', '♔'],
        [' ', ' ', ' '],
        [' ', ' ', '♙'],
    ])
    assert(blackTaken == ['♟'])
    assert(whiteTaken == [])
    assert(turn == "black")
    print("passed!")


def testChessMousePressed():
    print("testing mousepressed", end="...")
    initialBoard = [
        ['♟', '♚', '♟'],
        [' ', '♔', ' '],
        [' ', ' ', '♙'],
    ]
    app = PlayChess(copy.deepcopy(initialBoard), isTest=True)
    (board, blackTaken, whiteTaken, turn, time) = app.getState()
    assert(board == initialBoard)
    assert(blackTaken == whiteTaken == [])
    assert(turn == "white")

    # move the king to take the other pawn
    x, y = app.getCenterOfElementWithTag("board[1][1]")
    app.simulateMousePress(x, y)
    # clicking outside doesn't do anything
    app.simulateMousePress(5, 2)
    app.simulateMousePress(app.width-5, app.height-3)
    # move the piece since it's still selected
    x, y = app.getCenterOfElementWithTag("board[0][0]")
    app.simulateMousePress(x, y)
    (board, blackTaken, whiteTaken, turn, time) = app.getState()
    assert(board == [
        ['♔', '♚', '♟'],
        [' ', ' ', ' '],
        [' ', ' ', '♙'],
    ])
    assert(blackTaken == ['♟'])
    assert(whiteTaken == [])
    assert(turn == "black")

    # let's just move another piece
    x, y = app.getCenterOfElementWithTag("board[0][1]")
    app.simulateMousePress(x, y)
    x, y = app.getCenterOfElementWithTag("board[1][1]")
    app.simulateMousePress(x, y)
    (board, blackTaken, whiteTaken, turn, time) = app.getState()
    assert(board == [
        ['♔', ' ', '♟'],
        [' ', '♚', ' '],
        [' ', ' ', '♙'],
    ])
    print("passed!")


def testChessTimerFired():
    print("testing timerFired", end="...")
    initialBoard = [
        ['♟', '♚', '♟'],
        [' ', '♔', ' '],
        [' ', ' ', '♙'],
    ]
    app = PlayChess(copy.deepcopy(initialBoard), isTest=True)
    (board, blackTaken, whiteTaken, turn, time) = app.getState()
    assert(board == initialBoard)
    assert(blackTaken == whiteTaken == [])
    assert(turn == "white")
    assert(time == 20) # start out at 20 s

    # simulate time happening, which should affect the timer
    app.simulateTimerFire(1000)
    (board, blackTaken, whiteTaken, turn, time) = app.getState()
    assert(time == 20-1) # 1 second has elapsed so we only have 20 seconds left

    app.simulateTimerFire(900)
    (board, blackTaken, whiteTaken, turn, time) = app.getState()
    assert(time == 20-1) # not quite another full second, so it should still be 19

    app.simulateTimerFire(100)
    (board, blackTaken, whiteTaken, turn, time) = app.getState()
    assert(time == 20-2) # now it is 18

    app.simulateTimerFire(25*1000) # simulate a ton of time
    (board, blackTaken, whiteTaken, turn, time) = app.getState()
    assert(time == 0) # should still be 0

    # we make a move and the time resets to 20
    x, y = app.getCenterOfElementWithTag("board[1][1]")
    app.simulateMousePress(x, y)
    x, y = app.getCenterOfElementWithTag("board[0][0]")
    app.simulateMousePress(x, y)
    (board, blackTaken, whiteTaken, turn, time) = app.getState()
    assert(board == [
        ['♔', '♚', '♟'],
        [' ', ' ', ' '],
        [' ', ' ', '♙'],
    ])
    assert(time == 20) # yay!
    print("passed!")


def testPlayChess():
    print("testing PlayChess", end="...")
    testChessKeyPressed()
    # TODO: uncomment these when you're ready!
    testChessMousePressed()
    testChessTimerFired()
    print("passed!")

####################################
# Main
####################################


def main():
    testPlayChess()
    chessBoard = [
        ['♜','♞','♝','♛','♚','♝','♞','♜'],
        ['♟','♟','♟','♟','♟','♟','♟','♟'],
        [' ']*8,
        [' ']*8,
        [' ']*8,
        [' ']*8,
        ['♙','♙','♙','♙','♙','♙','♙','♙'],
        ['♖','♘','♗','♕','♔','♗','♘','♖']
    ]
    PlayChess(chessBoard, width=800, height=800)
    chessBoard = [
        ['♟', '♚', '♟'],
        [' ', '♔', ' '],
        [' ', ' ', '♙'],
    ]
    PlayChess(chessBoard, width=800, height=800)

if __name__ == "__main__":
    main()
