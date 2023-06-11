from tkinter import *
import random
from tkinter import messagebox

# these functions create the screen and adds the colour you want
GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 100
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

#this creates a window with title snake game
window = Tk()
window.title("Snake game")

# this creates the score and the first direction that the snake is going to go
score = 0
direction = 'right'

"""
This line creates a label widget using the Label class. It takes three parameters:window: It refers to the window or frame on which the label widget will be placed.
text="Score:{}".format(score): It sets the text that will be displayed on the label. The text is formatted using the format() method, where {} is a placeholder that will be replaced by the value of the score variable.
font=('consolas', 40): It specifies the font and size for the label text. In this case, it uses the font "consolas" with a size of 40.
label.pack(): This line packs or organizes the label widget within the window. It automatically determines the size required for the label based on its content and places it accordingly.
Overall, this code creates a label widget with the text "Score:" followed by the value of the score variable, formatted using the format() method. The label is then displayed within a window or frame.
"""
label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack()

# this code creates a canvas widget with a specific background color, height, and width. The canvas is then displayed within a window or frame using the pack() method. The canvas can be used to draw or display various graphical elements such as shapes, images, or text within the specified dimensions
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

def create_snake():
    '''
    This function initializes and creates a snake by generating a list of coordinates for its body parts,
    creating rectangle objects on a canvas with the specified coordinates, 
    and returning the initial coordinates and the identifiers of the created rectangles.
    '''
    coordinates = [[i*SPACE_SIZE, 0] for i in range(BODY_PARTS)][::-1]
    squares = []
    
    for x, y in coordinates:
        print(x,y)
        square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
        squares.append(square)
        print(squares)
    
    return coordinates, squares

def create_food():
    '''
    this creates the food
    '''
    x = random.randint(0, (GAME_WIDTH / SPACE_SIZE)-1) * SPACE_SIZE
    y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
    food_coordinates = [x, y]
    canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

    return food_coordinates

def next_turn(snake_coordinates, snake_squares, food_coordinates):
    '''
    this function updates the snake's position, handles collision checks,
      manages the game score, and schedules the next turn of the game.
    '''
    global score, direction

    x, y = snake_coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake_coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    snake_squares.insert(0, square)

    if x == food_coordinates[0] and y == food_coordinates[1]:
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food_coordinates = create_food()
    else:
        del snake_coordinates[-1]
        canvas.delete(snake_squares[-1])
        del snake_squares[-1]

    if check_collisions(snake_coordinates):
        game_over()
    else:
        window.after(SPEED, next_turn, snake_coordinates, snake_squares, food_coordinates)

def change_direction(new_direction):
    '''
    By performing these checks, the code ensures that the new direction is only accepted if it is different from
      the current direction and not opposite to it.
      This helps to prevent the snake from reversing its direction and colliding with itself immediately.
    '''
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def check_collisions(snake_coordinates):
    '''
    this function checks for collisions by examining the coordinates of the snake's head and comparing
      them against the boundaries of the game area and the coordinates of the snake's body parts.
      If any collision is detected, the function returns True; otherwise, it returns False.
    '''
    x, y = snake_coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake_coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def game_over():
    '''
    the game_over() function clears the canvas, displays a "YOUR A LOSER!" message in the center of the canvas,
     and shows an information dialog box to inform the player about the game over state an
    '''
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('consolas',70), text="YOUR A LOSER!", fill="red", tag="loser")
    messagebox.showinfo("", "Press 'r' to restart the game")

def restart_game(event):
    '''n of the game window, the event bindings for key presses,
     the creation of initial snake and food elements, and starts the game loop to control the game's flow.
    '''
    global score, direction
    score = 0
    direction = 'right'
    snake_coordinates, snake_squares = create_snake()
    canvas.delete(ALL)
    label.config(text="Score:{}".format(score))
    food_coordinates = create_food()
    next_turn(snake_coordinates, snake_squares, food_coordinates)

window_width = GAME_WIDTH
window_height = GAME_HEIGHT
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height + 50}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))
window.bind('r', restart_game)

snake_coordinates, snake_squares = create_snake()
food_coordinates = create_food()

next_turn(snake_coordinates, snake_squares, food_coordinates)

window.mainloop()
