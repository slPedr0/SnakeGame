from tkinter import *
from random import *
from playsound import *

# GAME SETTINGS

SCREEN_RESOLUTION = [1920, 1080]
GAME_WIDTH = 800
GAME_HEIGHT = 800
SPEED = 100
SPACE_SIZE = 40
INITIAL_BODY = 3
INITIAL_DIRECTION = "down"
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

# CLASSES AND FUNCTIONS

class Snake ():

    def __init__(self):
        self.body_size = INITIAL_BODY
        self.coordinates = []
        self.squares = []

        for i in range(0, INITIAL_BODY):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food():
    
    def __init__(self):

        x = randint(0,(GAME_WIDTH/SPACE_SIZE)-1)*SPACE_SIZE
        y = randint(0,(GAME_HEIGHT/SPACE_SIZE)-1)*SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=FOOD_COLOR, tag = "food")

def start():
    game_name.pack_forget()
    start_button.pack_forget()
    score_label.pack()
    canvas.pack()
    window.update()
    window.geometry(f"{GAME_WIDTH}x{GAME_HEIGHT+score_label.winfo_height()}+{int((SCREEN_RESOLUTION[0]-GAME_WIDTH)/2)}+{int((SCREEN_RESOLUTION[1]-(GAME_HEIGHT+score_label.winfo_height()))/2)}")
    play()

def play():
    global score 
    global direction
    canvas.delete(ALL)
    score = 0
    score_label.config(text=f"Score: {score}")

    direction = INITIAL_DIRECTION
    snake = Snake()
    food = Food()

    motion(snake, food)

def motion(snake, food):
    
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:

        global score
        score += 1
        score_label.config(text=f"Score: {score}")
        playsound("FoodCollect.mp3",False)
        canvas.delete("food")
        food = Food()
    
    else: 

        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_colision(snake):
        game_over()
    else:
        window.after(SPEED, motion, snake, food)

def change_direction(new_direction):

    global direction
    
    if new_direction == "left":
        if direction != "right":
            direction = new_direction
    if new_direction == "right":
        if direction != "left":
            direction = new_direction
    if new_direction == "up":
        if direction != "down":
            direction = new_direction
    if new_direction == "down":
        if direction != "up":
            direction = new_direction

def check_colision(snake):
    
    x, y = snake.coordinates[0]

    if x < 0 or x > GAME_WIDTH-1 or y < 0 or y > GAME_HEIGHT-1:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True    
    
    return False

def game_over():
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2-score_label.winfo_height(), text="GAME OVER", font=("Roboto", 70), fill="red", tag="gameover")
    canvas.create_window(canvas.winfo_width()/2, canvas.winfo_height()/2+20, window = playagain_button, tag="playagain_button")

# DISPLAY CONFIG

score = 0
direction = INITIAL_DIRECTION

window = Tk()
window.title("SNAKE GAME")
window.resizable(False, False)
window.config(bg="black")

score_label = Label(window, text=f"Score: {score}",font=("Roboto", 40))

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)

playagain_button = Button(window, text="Play Again", font=("Roboto", 20), bg="#AAAAAA", border=2, command= play)

game_name = Label(window, text="Snake Game", bg="black",fg= "green", font=("Roboto", 50), pady=100, padx=20)
game_name.pack()

start_button = Button(window, text="Play", font=("Roboto", 20), bg="#AAAAAA", width=10, border=2, command= start)
start_button.pack()

window.update()
window.geometry(f"{window.winfo_width()}x{window.winfo_width()}+{int((SCREEN_RESOLUTION[0]-window.winfo_width())/2)}+{int((SCREEN_RESOLUTION[1]-(window.winfo_width()))/2)}")

# KEY BINDING
window.bind("<w>", lambda event: change_direction("up"))
window.bind("<a>", lambda event: change_direction("left"))
window.bind("<s>", lambda event: change_direction("down"))
window.bind("<d>", lambda event: change_direction("right"))
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Down>", lambda event: change_direction("down"))
window.bind("<Right>", lambda event: change_direction("right"))

# Window position - 1920x1080 MONITOR

window.mainloop()