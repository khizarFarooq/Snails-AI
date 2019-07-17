import arcade
from copy import deepcopy
import random
from math import ceil,floor


class game_state:
    def __init__(self,board,agentPosition,humanPosition,turn,tt):
        self.board=board
        self.total_turns = tt
        self.agentPosition = agentPosition
        self.turn = turn
        self.humanPosition = humanPosition
        self.score = None

class MyGame(arcade.Window):
    
    def __init__(self, width, height, title,boardSize):

        # parent initilizer to make a gui of width and height
        super().__init__(width, height, title)

        # Set the background color
       # arcade.set_background_color(arcade.color.BLACK)

        self.UP = "UP"
        self.DOWN = "DOWN"
        self.RIGHT = "RIGHT"
        self.LEFT = "LEFT"
        self.boardSize = boardSize
        self.player_o_sprite=None
        self.player_x_sprite=None
        self.xes = None
        self.mucus = None
        self.oes = None

        # square with and height
        self.screen_width = width
        self.screen_height = height
        self.square_width = int(self.screen_width / self.boardSize)
        self.square_height = int(self.screen_height / self.boardSize)

        # Blue
        turn = 1
        self.agentTurn = 2
        self.redScore = 0
        self.blue_score = 0
        self.blue = (0,0)
        self.red=(boardSize-1,boardSize-1)
        self.total_turns = 0


        self.section = self.width/self.boardSize



        self.board = [[0 for i in range(self.boardSize)] for j in range(self.boardSize)]
        self.board[boardSize-1][boardSize-1] = 2
        self.board[0][0] = 1

        # initializing board state
        self.BoardState = game_state(deepcopy(self.board),deepcopy(self.red),deepcopy( self.blue),turn,self.total_turns)

    def setup(self):
        self.background_image = arcade.load_texture("images/background1.jpg")
        self.mucus = arcade.SpriteList()
        self.xes = arcade.SpriteList()
        self.oes = arcade.SpriteList()
        self.player_o_sprite = arcade.Sprite('images/blue_snail.png',0.170)
        self.player_o_sprite.center_x=int(0*self.section+self.section/2)
        self.player_o_sprite.center_y=int(0 * self.section+self.section/2)
        self.oes.append(self.player_o_sprite)

        self.player_x_sprite = arcade.Sprite('images/red_snail.png',0.170)
        self.player_x_sprite.center_x=int(7*self.section+self.section/2)
        self.player_x_sprite.center_y=int(7*self.section+self.section/2)
        self.xes.append(self.player_x_sprite)
        
    def on_mouse_press(self,x,y,buttonn,mofi):
        self.Check_in_Game_Matrix(x, y)
        pass

    def Check_in_Game_Matrix(self, x, y):
        col = x // self.square_width
        # y = self.screen_height - y
        row = y // self.square_height
        print("%s %s" % (row, col))
        print(self.BoardState.turn)
        st = self.original_place(self.BoardState)

        if self.BoardState.turn == 1:
            if (row==st[0]+1 and col==st[1]):
                self.MakeMove(self.UP)
            elif (row==st[0]-1 and col==st[1]):
                self.MakeMove(self.DOWN)
            elif (row==st[0] and col==st[1]-1):
                self.MakeMove(self.LEFT)
            elif (row==st[0] and col==st[1]+1):
                self.MakeMove(self.RIGHT)

        if self.BoardState.turn==2:

            children = self.generateChildren(self.BoardState)
            # print(children)
            for child in children:
                child.score = self.get_score(child, 6)
                print(child.board)

                agent = self.findAgent(child)
                mid = (self.boardSize // 2, self.boardSize // 2)
                distance=((mid[0]-agent[0])**2+(mid[1]-agent[1])**2)**0.5



                myscore = 0
                if self.BoardState.total_turns <= self.boardSize/2:
                    myscore = self.boardSize - ceil(distance)

                child.score += myscore

            fittestMoveScore = children[0].score
            index = 0
            for i in range(1, len(children)):
                if fittestMoveScore < children[i].score:
                    fittestMoveScore = children[i].score
                    index = i

            common = []
            for i in range(0, len(children)):
                if (fittestMoveScore == children[i].score):
                    common.append(children[i])
            index = random.randint(0,len(common) - 1)



            common[index].agentPosition
            originalPlace = self.BoardState.agentPosition
            NewPlace = common[index].agentPosition

            self.moveToNewPlace(originalPlace, NewPlace)
            self.BoardState.total_turns += 1

        pass

    def MakeMove(self,direction):
        original = self.original_place(self.BoardState)
        newPlace =  self.get_location(original,direction,False,self.BoardState)

        self.moveToNewPlace(original,newPlace)

    def original_place(self, state):
        if state.turn == 1:
            return state.humanPosition
        else:
            return state.agentPosition

    def get_location(self, original, direction, slide, state):

        if direction == self.UP:
            possiblePlace = (original[0] + 1, original[1])
            return self.makeItSmall(original, possiblePlace, slide, direction, state)

        if direction == self.DOWN:
            possiblePlace = (original[0] - 1, original[1])
            return self.makeItSmall(original, possiblePlace, slide, direction, state)

        if direction == self.LEFT:
            possiblePlace = (original[0], original[1] - 1)
            return self.makeItSmall(original, possiblePlace, slide, direction, state)

        if direction == self.RIGHT:
            possiblePlace = (original[0], original[1] + 1)
            return self.makeItSmall(original, possiblePlace, slide, direction, state)

    def makeItSmall(self,original,possiblePlace,slide,direction,state):
        if possiblePlace[1] < 0 or possiblePlace[1] > self.boardSize-1 or possiblePlace[0] < 0 or possiblePlace[0] > self.boardSize-1:
            if slide:
                return original
            return "Wrong move"
        if state.turn == 1:
            if state.board[possiblePlace[0]][possiblePlace[1]] == 11:
                return self.get_location(possiblePlace,direction,True,state)
            elif slide:
                return original
            elif state.board[possiblePlace[0]][possiblePlace[1]] == 22 or state.board[possiblePlace[0]][possiblePlace[1]] == 2:
                return "Wrong move"
            else:
                return possiblePlace
        if state.turn == 2:
            if state.board[possiblePlace[0]][possiblePlace[1]] == 22:
                return self.get_location(possiblePlace,direction,True,state)
            elif slide:
                return original
            elif state.board[possiblePlace[0]][possiblePlace[1]] == 11 or state.board[possiblePlace[0]][possiblePlace[1]] == 1:
                return "Wrong move"
            else:
                return possiblePlace

    def evaluateBoard(self,state):
        player= 0
        agent = (7,7)
        score = 0
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                if state.board[i][j] == 11 or state.board[i][j] == 1:
                    player +=1
                    score -= 1
                elif state.board[i][j] == 22 or state.board[i][j] == 2:
                    if state.board[i][j] == 2:
                        agent = (i,j)
                    score += 1
        return score

    def generateChildren(self,state):
        children = []
        original = self.original_place(state)
        newPlace =  self.get_location(original,self.UP,False,state)
        if newPlace != "Wrong move":
            newState = deepcopy(state)
            self.updateOriginalBoard(original,newPlace,newState)
            self.setNewPlace(newPlace,newState)
            children.append(newState)

        newPlace =  self.get_location(original,self.DOWN,False,state)
        if newPlace != "Wrong move":
            newState = deepcopy(state)
            self.updateOriginalBoard(original,newPlace,newState)
            self.setNewPlace(newPlace,newState)
            children.append(newState)

        newPlace =  self.get_location(original,self.LEFT,False,state)
        if newPlace != "Wrong move":
            newState = deepcopy(state)
            self.updateOriginalBoard(original,newPlace,newState)
            self.setNewPlace(newPlace,newState)
            children.append(newState)

        newPlace =  self.get_location(original,self.RIGHT,False,state)
        if newPlace != "Wrong move":
            newState = deepcopy(state)
            self.updateOriginalBoard(original,newPlace,newState)
            self.setNewPlace(newPlace,newState)
            children.append(newState)

        return children

    def huresticSearch(self,state):
        if self.coulumnAvailable(state,ceil((self.boardSize-1)/2)) >= self.boardSize/2 or self.coulumnAvailable(state,ceil((self.boardSize-1)/2)) >= self.boardSize/2 or self.rowAvailable(state,ceil((self.boardSize-1)/2)) >= self.boardSize/2 or self.rowAvailable(state,floor((self.boardSize-1)/2)) >= self.boardSize/2:
            return +3
        return 0

    def get_score(self, state, depth):
        if depth == 0:
            return self.evaluateBoard(state) + self.huresticSearch(state)

        self.changeTurn(state)

        if depth % 2 == 0:
            state.total_turns += 1
        children = self.generateChildren(state)

        for child in children:
            child.score = self.get_score(child, depth - 1)

        if state.turn == 2:
            return self.max(children)
        else:
            return self.min(children)

    def rowAvailable(self,state,index):
        number = 0
        for i in range(self.boardSize):
            if state.board[index][i] == 22 or state.board[index][i] == 2:
                number+=1
        return number

    def coulumnAvailable(self,state,index):
        number = 0
        for i in range(self.boardSize):
            if state.board[i][index] == 22 or state.board[i][index] == 2:
                number+=1
        return number

    def max(self, states):
        common = []
        fittestMoveScore = states[0].score
        index = 0
        for i in range(1, len(states)):
            if fittestMoveScore < states[i].score:
                fittestMoveScore = states[i].score
                index = i

        return fittestMoveScore

    def min(self, states):
        fittestMoveScore = states[0].score
        index = 0
        for i in range(1, len(states)):
            if fittestMoveScore > states[i].score:
                fittestMoveScore = states[i].score
                index = i
        return fittestMoveScore

    def moveToNewPlace(self,original,newPlace):
        if newPlace == "Wrong move":
            print("Wrong move")
            return
        
        if self.checkGameEnd(self.BoardState):
            print("GAME HAS ENDED")
            return

        # Move snail ahead on grid
        self.updateOriginalBoard(original,newPlace,self.BoardState)
        
        # Update places of snail heads
        self.setNewPlace(newPlace,self.BoardState)
        
        # print(newPlace)
        # self.printState(self.BoardState)

        # Print Trailing mucus
        self.printUpdatedOriginalBoard(original)

        # Make the Turn 
        self.updateSnailOnBoard(newPlace)

        #Update Score
        # self.updateScore()

        # Change Turn
        self.changeTurn(self.BoardState)

    def checkGameEnd(self,state):
        r = 0
        b = 0
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                if state.board[i][j] == 11 or state.board[i][j] == 1:
                    b += 1
                elif state.board[i][j] == 22 or state.board[i][j] == 2:
                    r += 1
        if r > 32 or b > 32:
            return True
        return False

    def updateOriginalBoard(self,original,newPlace,state):
        if state.turn == 1:
            state.board[newPlace[0]][newPlace[1]] = 1
            state.board[original[0]][original[1]] = 11
        elif state.turn == 2:
            state.board[newPlace[0]][newPlace[1]] = 2
            state.board[original[0]][original[1]] = 22

    def setNewPlace(self,nPlace,state):
        if state.turn == 1:
            state.humanPosition = nPlace
        else:
            state.agentPosition = nPlace

    def printUpdatedOriginalBoard(self,original):
        if (self.BoardState.turn == 2):
            mucus_red =  arcade.Sprite('images/red_splash.png',0.150)
            mucus_red.center_x = int(original[1] * self.section + self.section/2 )
            mucus_red.center_y = int(original[0] * self.section + self.section/2 )
            self.mucus.append(mucus_red)
            self.mucus.draw()
        else:
            mucus_blue =  arcade.Sprite('images/blue_splash.png',0.150)
            mucus_blue.center_x = int(original[1] * self.section + self.section/2 )
            mucus_blue.center_y = int(original[0] * self.section + self.section/2 )
            self.mucus.append(mucus_blue)
            self.mucus.draw()

    def updateSnailOnBoard(self,newPlace):
        if (self.BoardState.turn == 2):
            self.player_x_sprite.center_x = int(newPlace[1] * self.section + self.section/2 )
            self.player_x_sprite.center_y = int(newPlace[0] * self.section + self.section/2 )
        else:
            self.player_o_sprite.center_x = int(newPlace[1] * self.section + self.section/2 )
            self.player_o_sprite.center_y = int(newPlace[0] * self.section + self.section/2)

    def on_update(self, delta_time):
        self.oes.update()
        self.oes.update_animation()

    def printState(self,state):
        for i in range(self.boardSize-1,-1,-1):
            for j in range(self.boardSize):
                print(state.board[i][j],end='')
            print("\n",end='')
        print("\n\n",end='')

    def changeTurn(self,state):
        if state.turn == 1:
            state.turn = 2
        else:
            state.turn = 1

    def findAgent(self,state):
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                if state.board[i][j] == 2:
                    return (i,j)

    def on_draw(self):
        """ Called whenever we need to draw the window. """
        arcade.start_render()
        # Draw the background texture
        arcade.draw_texture_rectangle(self.width // 2, self.height // 2,
                                      self.width, self.height, self.background_image)
        self.mucus.draw()
        self.oes.draw()
        self.xes.draw()

        if self.checkGameEnd(self.BoardState):
            arcade.start_render()
            arcade.draw_text("GAME OVER", 140, 290, arcade.color.RED, 30)
            if self.BoardState.turn==1:
                arcade.draw_text("Agent Win !", 170, 240, arcade.color.WHITE, 20)
            elif self.BoardState.turn==2:
                arcade.draw_text("Human Win !", 170, 240, arcade.color.WHITE, 20)
            return 
        
        for i in range(0, self.width, int(self.width/self.boardSize)):
            arcade.draw_line(i,0,i,self.width,arcade.color.WHITE)
            arcade.draw_line(0,i,self.width,i,arcade.color.WHITE)
        
        # Initial place of red and blue snails
        section = self.width/self.boardSize


        self.xes.draw()
        self.oes.draw()

    def update(self, delta_time):
        pass

def main():
    window = MyGame(500, 500, "Snails",8)
    window.setup()
    arcade.run()

main()
