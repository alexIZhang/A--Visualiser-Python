import pygame
import math
from tkinter import *
from tkinter import messagebox as m_box

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
SCREEN.fill(white)

class Cell:
    def __init__(self, x, y):
        self.i = x
        self.j = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.cellColour = None
        self.obstacle = False
        self.neighbours = []
        self.parent = None

    def drawCell(self, colour, filled):
        i = self.i
        j = self.j
        #pygame.draw.rect(screen, [red, blue, green], [left, top, width, height], filled)
        pygame.draw.rect(SCREEN, colour, (i * cellW, j * cellH, cellW, cellH), filled)
        self.cellColour = colour
        pygame.display.update()

    def addNeighbours(self, grid):
        i = self.i
        j = self.j
        for xOff, yOff in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]:
            x = i + xOff
            y = j + yOff
            if x < 0 or x > rows-1 or y < 0 or y > columns-1 or grid[x][y].obstacle == True:
                continue
            self.neighbours.append(grid[x][y])

rows = 40
columns = 40
grid = [[0 for x in range(columns)] for y in range(rows)]
cellW = SCREEN_WIDTH / columns
cellH = SCREEN_HEIGHT / rows

for i in range(columns):
    for j in range(rows):
        grid[i][j] = Cell(i, j)

for i in range(columns):
    for j in range(rows):
        grid[i][j].drawCell(black, 1)

def start_end_init():
    global startNode
    global endNode    
    if startXBox.get() == '' or startYBox.get() == '' or endXBox.get() == '' or endYBox.get() == '':
        m_box.showwarning('Error','Fill the missing fields')
    if startXBox.get().isdigit() == False or startYBox.get().isdigit() == False or endXBox.get().isdigit() == False or endYBox.get().isdigit() == False:
        m_box.showwarning('Error', 'Values must be integers') 
    startX = int(startXBox.get())
    startY = int(startYBox.get())
    endX = int(endXBox.get())
    endY = int(endYBox.get())
    if startX < 0 or startX > rows-1 or startY < 0 or startY > columns-1 or endX < 0 or endX > rows-1 or endY < 0 or endY > columns-1:
        m_box.showwarning('Error', 'Values must between 0 and 39 inclusive') 
    startNode = grid[startX][startY]
    endNode = grid[endX][endY]
    window.quit()
    window.destroy()

window = Tk()
label = Label(window, text = 'Start X: ')
label1 = Label(window, text = 'Start Y: ')
startXBox = Entry(window)
startYBox = Entry(window)
label2 = Label(window, text = 'End X: ')
label3 = Label(window, text = 'End Y: ')
endXBox = Entry(window)
endYBox = Entry(window)
submit = Button(window, text='Submit', command = start_end_init)

label.grid(row = 0)
label1.grid(row = 1)
label2.grid(row = 2)
label3.grid(row = 3)
startXBox.grid(row = 0, column = 1, sticky = W)
startYBox.grid(row = 1, column = 1, sticky = W)
endXBox.grid(row = 2, column = 1, sticky = W)
endYBox.grid(row = 3, column = 1, sticky = W)
submit.grid(row = 4, columnspan = 1)

window.update()
window.mainloop()
pygame.init()

def setObstacle(position):
    g1 = int(position[0] / (400 / columns))
    g2 = int(position[1] / (400 / rows))
    cursorPos = grid[g1][g2]
    if cursorPos != startNode and cursorPos != endNode:
        if cursorPos.obstacle == False:
            cursorPos.obstacle = True
            cursorPos.drawCell(black, 0)
        else:
            cursorPos.obstacle = False
            cursorPos.drawCell(white, 0)
            cursorPos.drawCell(black, 1)

# Initialize both open and closed list
# Add the start node
# put the startNode on the openList 
openList = []
closedList = []
startNode.drawCell(red, 0)
endNode.drawCell(red, 0)
openList.append(startNode)

pregame = True
while pregame:
    for event in pygame.event.get():
        if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:
            position = pygame.mouse.get_pos()
            setObstacle(position)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pregame = False
        if event.type == pygame.QUIT:
            pygame.quit()

for i in range(columns):
    for j in range(rows):
        grid[i][j].addNeighbours(grid)
                
def main():
    # while the openList is not empty
    # using if since already looping through main
    if len(openList) > 0:
        # Get the current node
        # let the currentNode equal the node with the least f value
        # remove the currentNode from the openList
        # add the currentNode to the closedList
        currNode = openList[0]
        for openNode in openList:
            if openNode.f < currNode.f:
                currNode = openNode

        openList.remove(currNode)
        closedList.append(currNode)
        
        # If current node is goal, backtrack for path
        if currNode == endNode:
            # backtracking through previous nodes
            total_distance = currNode.g
            while currNode != startNode:
                currNode.drawCell(red, 0)
                currNode = currNode.parent
            Tk().wm_withdraw()
            m_box.showinfo('Done!', ('The end node was ' + str(total_distance) + ' cells from the start'))
            pygame.quit()
            
        # For each neighbour 
        neighbours = currNode.neighbours
        for neighbour in neighbours:
            # If child is on the closedList, continue
            if neighbour in closedList:
                continue
            
            # if child.position is in the openList's nodes positions
            # if the child.g is higher than the openList node's g
            # continue to beginning of for loop  
            # add child to the open list
            candidateG = currNode.g + 1
            if neighbour not in openList:
                openList.append(neighbour)
            elif candidateG >= neighbour.g:
                continue

            # Create f, g, h values
            # child.g = currentNode.g + distance between child and current
            # child.h = distance from child to end
            # child.f = child.g + child.h
            # Update each neighbour's parent
            neighbour.g = candidateG
            neighbour.h = math.sqrt((neighbour.i - endNode.i)**2 + (neighbour.j - endNode.j)**2)
            neighbour.f = neighbour.g + neighbour.h
            if neighbour.parent == None:
                neighbour.parent = currNode
            
    for openNode in openList:
        if openNode.cellColour != green:
            openNode.drawCell(green, 0)
            openNode.drawCell(black, 1)
            openNode.cellColour = green
    for closedNode in closedList:
        if closedNode != startNode and closedNode.cellColour != blue:
            closedNode.drawCell(blue, 0)
            closedNode.drawCell(black, 1)
            closedNode.cellColour = blue
            
while True:
    ev = pygame.event.poll()
    if ev.type == pygame.QUIT:
        pygame.quit()
    main()
    pygame.time.delay(10)
    pygame.display.update()

        


