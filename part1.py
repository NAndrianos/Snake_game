# Group#: G37
# Student Names: Ryley McRae & Niko Andrianos

"""
    This program implements a variety of the snake 
    game (https://en.wikipedia.org/wiki/Snake_(video_game_genre))
"""

import threading
import queue        #the thread-safe queue from Python standard library

from tkinter import Tk, Canvas, Button
import random, time

class Gui():
    """
        This class takes care of the game's graphic user interface (gui)
        creation and termination.
    """
    def __init__(self, queue, game):
        """        
            The initializer instantiates the main window and 
            creates the starting icons for the snake and the prey,
            and displays the initial gamer score.
        """
        #some GUI constants
        scoreTextXLocation = 60
        scoreTextYLocation = 15
        textColour = "white"
        #instantiate and create gui
        self.root = Tk()
        self.canvas = Canvas(self.root, width = WINDOW_WIDTH, 
            height = WINDOW_HEIGHT, bg = BACKGROUND_COLOUR)
        self.canvas.pack()
        #create starting game icons for snake and the prey
        self.snakeIcon = self.canvas.create_line(
            (0, 0), (0, 0), fill=ICON_COLOUR, width=SNAKE_ICON_WIDTH)
        self.preyIcon = self.canvas.create_rectangle(
            0, 0, 0, 0, fill=ICON_COLOUR, outline=ICON_COLOUR)
        #display starting score of 0
        self.score = self.canvas.create_text(
            scoreTextXLocation, scoreTextYLocation, fill=textColour, 
            text='Your Score: 0', font=("Helvetica","11","bold"))
        #binding the arrow keys to be able to control the snake
        for key in ("Left", "Right", "Up", "Down"):
            self.root.bind(f"<Key-{key}>", game.whenAnArrowKeyIsPressed)

    def gameOver(self):
        """
            This method is used at the end to display a
            game over button.
        """
        gameOverButton = Button(self.canvas, text="Game Over!", 
            height = 3, width = 10, font=("Helvetica","14","bold"), 
            command=self.root.destroy)
        self.canvas.create_window(200, 100, anchor="nw", window=gameOverButton)
    

class QueueHandler():
    """
        This class implements the queue handler for the game.
    """
    def __init__(self, queue, gui):
        self.queue = queue
        self.gui = gui
        self.queueHandler()
    
    def queueHandler(self):
        '''
            This method handles the queue by constantly retrieving
            tasks from it and accordingly taking the corresponding
            action.
            A task could be: game_over, move, prey, score.
            Each item in the queue is a dictionary whose key is
            the task type (for example, "move") and its value is
            the corresponding task value.
            If the queue.empty exception happens, it schedules 
            to call itself after a short delay.
        '''
        try:
            while True:
                task = self.queue.get_nowait()
                if "game_over" in task:
                    gui.gameOver()
                elif "move" in task:
                    points = [x for point in task["move"] for x in point]
                    gui.canvas.coords(gui.snakeIcon, *points)
                elif "prey" in task:
                    gui.canvas.coords(gui.preyIcon, *task["prey"])
                elif "score" in task:
                    gui.canvas.itemconfigure(
                        gui.score, text=f"Your Score: {task['score']}")
                self.queue.task_done()
        except queue.Empty:
            gui.root.after(100, self.queueHandler)


class Game():
    '''
        This class implements most of the game functionalities.
    '''
    def __init__(self, queue):
        """
           This initializer sets the initial snake coordinate list, movement
           direction, and arranges for the first prey to be created.
        """
        self.queue = queue
        self.score = 0
        #starting length and location of the snake
        #note that it is a list of tuples, each being an
        # (x, y) tuple. Initially its size is 5 tuples.       
        self.snakeCoordinates = [(495, 55), (485, 55), (475, 55),
                                 (465, 55), (455, 55)]
        #initial direction of the snake
        self.direction = "Left"
        self.gameNotOver = True
        self.createNewPrey()

    def superloop(self) -> None:
        """
            This method implements a main loop
            of the game. It constantly generates "move" 
            tasks to cause the constant movement of the snake.
            Use the SPEED constant to set how often the move tasks
            are generated.
        """
        SPEED = 0.15     #speed of snake updates (sec)
        while self.gameNotOver:
            #complete the method implementation below
            self.move()
            time.sleep(SPEED)

    def whenAnArrowKeyIsPressed(self, e) -> None:
        """ 
            This method is bound to the arrow keys
            and is called when one of those is clicked.
            It sets the movement direction based on 
            the key that was pressed by the gamer.
            Use as is.
        """
        currentDirection = self.direction
        #ignore invalid keys
        if (currentDirection == "Left" and e.keysym == "Right" or 
            currentDirection == "Right" and e.keysym == "Left" or
            currentDirection == "Up" and e.keysym == "Down" or
            currentDirection == "Down" and e.keysym == "Up"):
            return
        self.direction = e.keysym

    def move(self) -> None:
        """ 
            This method implements what is needed to be done
            for the movement of the snake.
            It generates a new snake coordinate. 
            If based on this new movement, the prey has been 
            captured, it adds a task to the queue for the updated
            score and also creates a new prey.
            It also calls a corresponding method to check if 
            the game should be over. 
            The snake coordinates list (representing its length 
            and position) should be correctly updated.
        """
        def isPreyCaptured(snakeCoordinates) -> bool:
            snakeX = snakeCoordinates[0]
            snakeY = snakeCoordinates[1]
            if snakeX < self.preyCoordinates[0] or snakeX > self.preyCoordinates[2]:
                return False # head not in the same column
            if snakeY < self.preyCoordinates[1] or snakeY > self.preyCoordinates[3]:
                return False # head not in the same row
            return True 

        # calculate the new coordinate of the snake head
        newSnakeCoordinates = self.calculateNewCoordinates()

        # based on the new coordinates, check if the prey is captured
        if isPreyCaptured(newSnakeCoordinates):
            # if so, update score, create new prey, and add "score" task to the queue
            self.score += 1
            self.createNewPrey()
            self.queue.put({"score": self.score})
            # if the snake captures the prey, the tail stays in place (do nothing)
        else:
            # otherwise, we update the location of the tail by removing the first segment
            self.snakeCoordinates.pop(0)

        # next, update the location of the head of the snake. this is done after
        # updating the location of the tail to avoid a bug where isGameOver()
        # will think the snake has bitten its tail, but in fact, 
        # the tail has not yet been updated. in this case, the game would essentially
        # consider the snake as 1 segment longer than it actually is
        self.snakeCoordinates.append(newSnakeCoordinates)
        if not self.isGameOver(newSnakeCoordinates):
            self.queue.put({"move": self.snakeCoordinates})

    def calculateNewCoordinates(self) -> tuple:
        """
            This method calculates and returns the new 
            coordinates to be added to the snake
            coordinates list based on the movement
            direction and the current coordinate of 
            head of the snake.
            It is used by the move() method.    
        """
        lastX, lastY = self.snakeCoordinates[-1]
        #complete the method implementation below

        # Check which direction the snake is moving in
        if self.direction == "Up":
            return lastX, lastY - SNAKE_ICON_WIDTH
        elif self.direction == "Right":
            return lastX + SNAKE_ICON_WIDTH, lastY
        elif self.direction == "Left":
            return lastX - SNAKE_ICON_WIDTH, lastY
        else:
            return lastX, lastY + SNAKE_ICON_WIDTH

    def isGameOver(self, snakeCoordinates) -> None:
        """
            This method checks if the game is over by 
            checking if now the snake has passed any wall
            or if it has bit itself.
            If that is the case, it updates the gameNotOver 
            field and also adds a "game_over" task to the queue. 
        """
        x, y = snakeCoordinates
        #complete the method implementation below

        # If out of bounds or snake bites itself end else do nothing
        #NOTE: Assume the head of the snake is last element
        # Since the snake cannot bite it's own head check if
        # the coordinates are apart of the snakes tail.
        if (x > WINDOW_WIDTH or x < 0 or
            y > WINDOW_HEIGHT or y < 0 or
            any(coord[0] == x and coord[1] == y for coord in self.snakeCoordinates[:-1])):

            self.gameNotOver = False
            self.queue.put({"game_over": None}) # Add to game queue to trigger GUI exit

    def createNewPrey(self) -> None:
        """ 
            This methods picks an x and a y randomly as the coordinate 
            of the new prey and uses that to calculate the 
            coordinates (x - 5, y - 5, x + 5, y + 5). 
            It then adds a "prey" task to the queue with the calculated
            rectangle coordinates as its value. This is used by the 
            queue handler to represent the new prey.                    
            To make playing the game easier, set the x and y to be THRESHOLD
            away from the walls. 
        """
        THRESHOLD = 15   #sets how close prey can be to borders
        #complete the method implementation below

        # Get a random x and y a threshold away from the window
        x = random.randint(THRESHOLD//5, (WINDOW_WIDTH-THRESHOLD)//5)*5
        y = random.randint(THRESHOLD//5, (WINDOW_HEIGHT-THRESHOLD)//5)*5
        self.preyCoordinates = (x - 5, y - 5, x + 5, y + 5)
        self.queue.put({"prey": self.preyCoordinates}) # Add prey to game queue
        print(f"prey: {self.preyCoordinates}")

if __name__ == "__main__":
    #some constants for our GUI
    WINDOW_WIDTH = 500           
    WINDOW_HEIGHT = 300 
    SNAKE_ICON_WIDTH = 15
    
    BACKGROUND_COLOUR = "green"   #you may change this colour if you wish
    ICON_COLOUR = "yellow"        #you may change this colour if you wish

    gameQueue = queue.Queue()     #instantiate a queue object using python's queue class

    game = Game(gameQueue)        #instantiate the game object

    gui = Gui(gameQueue, game)    #instantiate the game user interface
    
    QueueHandler(gameQueue, gui)  #instantiate our queue handler    
    
    #start a thread with the main loop of the game
    threading.Thread(target = game.superloop, daemon=True).start()

    #start the GUI's own event loop
    gui.root.mainloop()