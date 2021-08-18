from Node import Node
import pygame, sys
pygame.init()

class Pathfinder:
    def __init__(self, numCols=24, numRows=24, nodesize=25, screensize=600):
        self.NUM_COLS = numCols
        self.NUM_ROWS = numRows
        self.NODE_SIZE = nodesize
        self.SCREEN_SIZE = screensize
        self.SCREEN = pygame.display.set_mode((600, 600))
        self.grid = []
        self.startNode = None
        self.endNode = None

        self.running = True
        self.pathFound = False
        self.canDraw = True


    def createNodes(self):
        for r in range(self.NUM_ROWS):
            self.grid.append([])
            for c in range(self.NUM_COLS):
                self.grid[r].append(Node(r=r, c=c, screen=self.SCREEN))


    def setStartNode(self, row, col):
        self.startNode = self.grid[row][col]
        self.startNode.status = 'start'
        self.startNode.gcost = 0


    def setEndNode(self, row, col):
        self.endNode = self.grid[row][col]
        self.endNode.status = 'end'

        # set all hcosts
        for n in self.grid:
            for m in n:
                m.set_hcost(self.endNode)
                

    def setWallNode(self, n):
        if n == self.startNode or n == self.endNode:
            return

        n.status = 'white'

        return


    def drawNodes(self):
        # draw nodes
        for row in self.grid:
            for n in row:
                if n.status == None:
                    color = (0,0,0)
                elif n.status == 'red':
                    color = (200,0,0)
                elif n.status == 'green':
                    color = (0,200,0)  
                elif n.status == 'start':
                    color = (0,0,200)
                elif n.status == 'end':
                    color = (0,0,100)
                elif n.status == 'white':
                    color = (220,220,220)
                else:
                    color = (200,200,0) # this should never happen and will show up as yellow

                pygame.draw.rect(self.SCREEN, color, (n.X, n.Y, n.SIZE, n.SIZE))

        # draw grid lines
        for i in range(int(self.NODE_SIZE), self.SCREEN_SIZE, int(self.NODE_SIZE)):
            pygame.draw.line(self.SCREEN, (255,255,255), (i, 0), (i, self.SCREEN_SIZE)) # vertical lines
            pygame.draw.line(self.SCREEN, (255,255,255), (0,i), (self.SCREEN_SIZE, i)) # horizontal lines

    
    def chooseNextNode(self):
        # loop through the grid (only looking at 'green' nodes)
        # keep track of min fcost
        bestChoice = None

        for row in self.grid:
            for n in row:
                if n.status == 'green':
                    if bestChoice == None:
                        bestChoice = n
                    elif bestChoice.fcost == n.fcost:
                        if n.hcost < bestChoice.hcost:
                            bestChoice = n
                    elif n.fcost < bestChoice.fcost:
                        bestChoice = n

        # if bestChoice is the end node: 
        return bestChoice


    def selectNode(self, r, c):

        # if self.grid[r][c] == self.endNode:
        #     self.pathFound = True
        #     self.showPath(self.grid[r][c])

        # node.status = 'red'
        self.grid[r][c].status = 'red'

        # create a list of diagonal neighbors and a list of edge neighbors
        diagonals = []
        edges = []
        # diag neighbors
        if r > 0:
            if c > 0:
                diagonals.append(self.grid[r-1][c-1])
            if c < self.NUM_COLS - 1:
                diagonals.append(self.grid[r-1][c+1])
        if r < self.NUM_ROWS - 1:
            if c > 0:
                diagonals.append(self.grid[r+1][c-1])
            if c < self.NUM_COLS - 1:
                diagonals.append(self.grid[r+1][c+1])
        # edge neighbors
        if r > 0:
            edges.append(self.grid[r-1][c])
        if r < self.NUM_ROWS - 1:
            edges.append(self.grid[r+1][c])
        if c > 0:
            edges.append(self.grid[r][c-1])
        if c < self.NUM_COLS - 1:
            edges.append(self.grid[r][c+1])

        # for each diag neighbor: status='green', gcost = currentNode.gcost+14 (if neighbor.gcost is None or is greater than the new gcost), update fcost
        for n in diagonals:
            # ignore wall nodes
            if n.status == 'white' or n.status == 'red':
                continue

            n.status = 'green'
            newg = self.grid[r][c].gcost + 14 
            if n.gcost == None or n.gcost > newg:
                n.gcost = newg
                # update fcost
                n.update_fcost()
                # set n.prev to point at the current node
                n.prev = self.grid[r][c]
            
            # if n is the endNode: call showPath(n)
            if n == self.endNode:
                self.pathFound = True
                self.showPath(n)

        # same for edge neighbors, except add 10 instead of 14
        for n in edges:
            # ignore wall nodes
            if n.status == 'white' or n.status == 'red':
                continue

            n.status = 'green'
            newg = self.grid[r][c].gcost + 10 
            if n.gcost == None or n.gcost > newg:
                n.gcost = newg
                # update fcost
                n.update_fcost()
                # set n.prev to point at the current node
                n.prev = self.grid[r][c]

            # # if n is the endNode: call showPath(n)
            if n == self.endNode:
                self.pathFound = True
                self.showPath(n)

    def showPath(self, n):
        if n == self.startNode:
            return
        else:
            n.status = 'yellow'
            self.showPath(n.prev)


    def getClickedNode(self, mpos):
        """
        mpos is the mouse position as (x,y).
        return the node that contains that point
        """

        c = mpos[0] // 25 
        r = mpos[1] // 25

        return self.grid[r][c]
            

    def runSim(self):
        self.createNodes()
        self.setStartNode(2,2)
        self.setEndNode(20,17)

        # select start node
        self.selectNode(self.startNode.ROW, self.startNode.COL)

        while self.running:
            # did the user click the close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and not self.pathFound:
                    if event.key == pygame.K_SPACE:
                        # set canDraw to False so walls cannot be added
                        self.canDraw = False

                elif event.type == pygame.MOUSEBUTTONDOWN and self.canDraw:
                    clickedNode = self.getClickedNode(pygame.mouse.get_pos())
                    self.setWallNode(clickedNode)

            if not self.canDraw and not self.pathFound:
                # Choose the next node and select it
                nextNode = self.chooseNextNode()
                self.selectNode(nextNode.ROW, nextNode.COL)
                # pause screen
                # pygame.time.wait(30)

            # create a gray bg
            self.SCREEN.fill((30, 30, 30))

            self.drawNodes()

            # flip the display
            pygame.display.flip()

        # Quit
        pygame.quit()



pf = Pathfinder()
pf.runSim()
