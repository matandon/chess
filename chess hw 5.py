import basic_graphics

def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

def drawChessBoard(canvas, width, height, board, color, margin):
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
            x1, y1 = (j*cellWidth) + margin, (i*cellHeight) + margin
            x2, y2 = x1+cellWidth, y1+cellHeight
            if (i+j)%2 == 0: 
                canvas.create_rectangle(x1,y1,x2,y2,width=0,fill="white")
            else: 
                canvas.create_rectangle(x1,y1,x2,y2,fill=cellColor,width=0)
            canvas.create_text((x1+x2)//2, (y1+y2)//2, text=board[i][j], font=f"Arial {fontSize}")
    
def getStandardChessBoard():
    return [
        ['♜','♞','♝','♛','♚','♝','♞','♜'],
        ['♟','♟','♟','♟','♟','♟','♟','♟'],
        [' ']*8,
        [' ']*8,
        [' ']*8,
        [' ']*8,
        ['♙','♙','♙','♙','♙','♙','♙','♙'],
        ['♖','♘','♗','♕','♔','♗','♘','♖']
    ]

def getSimplifiedChessBoard():
    return [
        ['♜','♞','♝','♛','♚','♝','♞','♜'],
        ['♟','♟','♟','♟','♟','♟','♟','♟'],
        [' ']*8,
        [' ']*8,
        [' ']*8,
        ['♙','♙','♙','♙','♙','♙','♙','♙'],
        ['♖','♘','♗','♕','♔','♗','♘','♖']
    ]

def getSolitaireChessBoard():
    return [
        [' ']*4,
        [' ','♝',' ',' '],
        ['♜','♟',' ',' '],
        [' ',' ',' ','♞'],
    ]

def testDrawChessBoard():
    print("Testing drawChessBoard()...")
    print("Since this is graphics, this test is not interactive.")
    print("Inspect each of these results manually to verify them.")
    basic_graphics.run(getStandardChessBoard(), (0,112,255), 20,
        drawFn=drawChessBoard,width=500,height=500
    )
    basic_graphics.run(getSolitaireChessBoard(), (255,150,0), 0,
        drawFn=drawChessBoard,width=150,height=150
    )
    basic_graphics.run(getSimplifiedChessBoard(), (10,255,0), 30,
        drawFn=drawChessBoard,width=300,height=260
    )
    print("Done!")

testDrawChessBoard()

