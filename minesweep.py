from turtle import Turtle, Screen
from random import randint
from math import ceil
import time

t = Turtle('square', visible=False)
s = Screen()
# s.tracer(False)
t.pu()
flag = Turtle('circle', visible=False)
flag.pu()
score = Turtle(visible=False)
score.pu()
numFlag = Turtle(visible=False)
numFlag.pu()

timez = 1
WON = False

SIZE = 15
MULT = 600 / SIZE
PROB = 20
FCOLOR = "red"
FSHAPE = "triangle"

def scored():
    global timez
    # s.ontimer(scored, None)
    # print("+")
    score.goto(351, 240)
    score.clear()
    if not WON:
        score.write(timez, False, align="center", font=("Dubai Medium", 25))
        timez += 1
        s.update()
    s.ontimer(scored, 1000)

def win():
    global WON
    try:
        print(trueMines, flagged)
        if all([True if (x[0] + MULT / 2, x[1] + MULT / 2) in [y[0] for y in trueMines] else False for x in flagged]) and flagged != {} and len(flagged) == len(trueMines):
            t.goto(0, 0)
            if not WON:
                s.clearscreen()
                s.reset()
                t.write("you won lmao")
                s.ontimer(end, 5000)
            WON = True

        else:
            print([y[0] for y in trueMines])
    except:
        pass
    finally:
        s.ontimer(win, 100)
    
def showFlags(numMines):
    # global numMines
    X, Y = (350, 210)
    numFlag.goto(X, Y + 28)
    numFlag.clear()
    numFlag.shape(FSHAPE)
    numFlag.color("red")
    numFlag.setheading(90)
    numFlag.shapesize(0.8)
    numFlag.stamp()
    numFlag.color("black")
    numFlag.goto(X + 25 + 5 * len(str(numMines)), Y)
    numFlag.write(numMines, False, align="center", font=("Dubai Medium", 25))
    s.update()

def draw(color):
    t.color(color)
    t.stamp()
    s.update()

def flagon():
    global flagStamp
    flag.color(FCOLOR)
    flag.goto(350, 300)
    flagStamp = flag.stamp()

def flagoff():
    global flagStamp
    flag.color(FCOLOR)
    flag.goto(350, 300)
    flag.shapesize(1.15)
    flag.stamp()
    flag.color(FCOLOR, "white")
    flag.shapesize(1)
    flag.goto(350, 300)
    try:
        flag.clearstamp(flagStamp)
    except: pass
    flagStamp = flag.stamp()
    s.update()

def run():
    global mines, MULT, SIZE, FLAGGING, numMines, trueMines
    FLAGGING = False
    t.goto(0, 0)
    t.shapesize(30)

    draw('grey')
    
    t.color('black')

    allSquares = []

    for x in range(SIZE + 1):
        for y in range(SIZE + 1):
            if x < SIZE and y < SIZE:
                allSquares.append((-300 + (x + 1) * MULT, -300 + (y + 1) * MULT))
            t.goto(-300, -300 + y * MULT)
            t.pd()
            t.goto(300, -300 + y * MULT)
            t.pu()
        t.goto(-300 + x * MULT, -300)
        t.pd()
        t.goto(-300 + x * MULT, 300)
        t.pu()


    mines = [True if randint(1, 100) <= PROB + 1 else False for i in range(len(allSquares))]
    numMines = sum([1 for x in mines if x])
    print(numMines)

    '''
    mines is a dictionary: {(x, y):mine status}
    '''
    mines = list(zip(allSquares, mines, [0 for i in range(len(allSquares))]))
    trueMines = [x for x in mines if x[1]]
    print(trueMines)

def getNear(x, y):
    n = 0
    lots = []
    for a in range(-1, 2):
        for b in range(-1, 2):
            back = x - a * MULT
            down = y - b * MULT
            if back > -300 and down > -300:
                for ((c, d), isMine, popped) in mines:
                    if (c, d) == (back, down):
                        lots.append(((c, d), isMine, popped))
                        # print(back, down, c, d)
                        if isMine:
                            n += 1
    return (n, lots)

def end():
    global timez, numMines, flagged, WON
    timez = 1
    WON = False
    flagged = {}
    t.shape("square")
    s.clearscreen()
    s.tracer(False)
    s.listen()
    s.onscreenclick(clicked)
    s.onscreenclick(handleRight, 3)
    s.onkeypress(switch, "c")
    
    # s.ontimer(scored, 1000)
    run()
    showFlags(numMines)
    flagoff()
    s.mainloop()

def clicked(x, y):
    global numMines
    for ((a, b), isMine, popped) in mines:
        if x < a and y < b and x > -300 and y > -300 and x < 300 and y < 300:
            if isMine and not FLAGGING:
                t.goto(a - MULT / 2, b - MULT /2)
                if t.pos() not in flagged:
                    t.color("red")
                    t.write("died")
                    end()
            else:
                if not popped:
                    nearest, allNear = getNear(a, b)
                    t.goto(a - MULT / 2, b - MULT / 2)
                    if FLAGGING:
                        t.shapesize(30 * 0.95 / SIZE)
                        # print(t.pos(), flagged, t.pos() in flagged)
                        t.shape(FSHAPE)
                        t.setheading(0)
                        t.shapesize(0.8)
                        if t.pos() not in flagged and numMines != 0:
                            t.color(FCOLOR)
                            flagged.update({t.pos():t.stamp()})
                            numMines -= 1
                            showFlags(numMines)
                            
                        elif t.pos() in flagged:
                            t.clearstamp(flagged.get(t.pos()))
                            t.color("grey")
                            flagged.pop(t.pos())
                            numMines += 1
                            showFlags(numMines)
                            
                        s.update()
                    else:
                        t.shape("square")
                        t.setheading(0)
                        if t.pos() not in flagged:
                            t.color("white")
                            t.shapesize(30 * 0.95/SIZE)
                            t.stamp()
                            # s.update()
                            t.color("black")
                            if nearest != 0: t.write(nearest)
                            PLACE = mines.index(((a, b), isMine, popped))
                            mines.pop(PLACE)
                            mines.insert(PLACE, ((a, b), isMine, True))
                            if nearest == 0:
                                for ((x, y), isMine, popped) in allNear:
                                    reveal(x, y)
            # s.update()
            # print(a, b)
            
            break

def reveal(x, y):
    global numMines
    for ((a, b), isMine, popped) in mines:
        if x <= a and y <= b and x > -300 and y > -300:
            if not popped and not isMine:
                nearest, allNear = getNear(a, b)
                t.goto(a - MULT / 2, b - MULT / 2)
                if t.pos() in flagged: 
                    flagged.pop(t.pos())
                    numMines += 1
                    showFlags(numMines)
                t.color("white")
                t.shape("square")
                t.shapesize(30 * 0.95/SIZE)
                t.stamp()
                t.color("black")
                if nearest != 0: t.write(nearest)
                PLACE = mines.index(((a, b), isMine, popped))
                mines.pop(PLACE)
                mines.insert(PLACE, ((a, b), isMine, True))
                if nearest == 0:
                    for ((x, y), isMine, popped) in allNear:
                        reveal(x, y)
            # print(a, b)
            break

def switch():
    global FLAGGING
    # s.onkey(None, "c")
    if FLAGGING:
        FLAGGING = False
        flagoff()
    else:
        FLAGGING = True
        flagon()
    print(FLAGGING)
    # s.onkey(switch, "c")

def handleRight(x, y):
    switch()
    clicked(x, y)
    switch()

scored()
win()
end()

# flagoff()

# s.listen()
# s.onscreenclick(clicked)
# s.onkeypress(switch, "c")
# s.ontimer(scored, 1/300)

# s.mainloop()