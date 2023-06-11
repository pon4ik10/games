from tkinter import *
import random
from tkinter import messagebox

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 50
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

window = Tk()
window.title("Snake game")
window.resizable(False, False)

score = 0
direction = 'down'

label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

def create_snake():
    coordinates = [[0, 0]] * BODY_PARTS
    squares = []
    for x, y in coordinates:
        square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
        squares.append(square)
    return coordinates, squares

def create_food():
    x = random.randint(0, (GAME_WIDTH / SPACE_SIZE)-1) * SPACE_SIZE
    y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
    food_coordinates = [x, y]
    canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")
    return food_coordinates

def next_turn(food_coordinates):
    global score, direction, snake_coordinates, snake_squares

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

    if check_collisions():
        game_over()
    else:
        window.after(SPEED, next_turn, food_coordinates)

def change_direction(new_direction):
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

def check_collisions():
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
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('consolas',70), text="GAME OVER", fill="red", tag="gameover")
    messagebox.showinfo("GAME OVER", "Press 'r' to restart the game")

def restart_game(event):
    global score, snake_coordinates, snake_squares
    score = 0
    snake_coordinates, snake_squares = create_snake()
    canvas.delete(ALL)
    label.config(text="Score:{}".format(score))
    food_coordinates = create_food()
    next_turn(food_coordinates)

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))
window.bind('r', restart_game)

snake_coordinates, snake_squares = create_snake()
food_coordinates = create_food()

next_turn(food_coordinates)

window.mainloop()
