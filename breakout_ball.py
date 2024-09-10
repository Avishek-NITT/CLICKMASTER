import tkinter as tk

root = tk.Tk()
root.title("Breakout Ball")

# Global constants

height = 700
width = 1000
ball_diameter = 20  # Diameter of the ball
player_width = 20
player_height = 100
player_speed = 20  # Speed at which the player moves
key_history = []



# Calculate initial ball position to be centered
ball_radius = ball_diameter / 2
center_x = width / 2
center_y = height / 2
x0 = center_x - ball_radius
y0 = center_y - ball_radius
x1 = center_x + ball_radius
y1 = center_y + ball_radius

# Player initial positions
left_player_x0 = 10
left_player_x1 = left_player_x0 + player_width
right_player_x0 = width - 10 - player_width
right_player_x1 = right_player_x0 + player_width

# Canvas
canvas = tk.Canvas(root, bg="black", width=width, height=height)
canvas.pack()

# Create ball
ball = canvas.create_oval(x0, y0, x1, y1, fill="white")

# Create players
left_player = canvas.create_rectangle(left_player_x0, center_y - player_height / 2, left_player_x1, center_y + player_height / 2, fill="blue")
right_player = canvas.create_rectangle(right_player_x0, center_y - player_height / 2, right_player_x1, center_y + player_height / 2, fill="red")

dx, dy = 5, 5  # Ball speed

def reset_game():
    # Reset ball to center
    center_x = width / 2
    center_y = height / 2
    global x0, y0, x1, y1
    x0 = center_x - ball_radius
    y0 = center_y - ball_radius
    x1 = center_x + ball_radius
    y1 = center_y + ball_radius
    canvas.coords(ball, x0, y0, x1, y1)
    
    # Reset ball movement direction
    global dx, dy
    dx, dy = 5, 5

def move_ball():
    global x0, y0, x1, y1, dx, dy
    
    # Move ball by updating its coordinates
    canvas.move(ball, dx, dy)
    
    # Get current position of the ball
    pos = canvas.coords(ball)
    x0, y0, x1, y1 = pos
    
    # Check for collision with left player
    left_player_coords = canvas.coords(left_player)
    if (x1 >= left_player_coords[0] and x0 <= left_player_coords[2]) and (y1 >= left_player_coords[1] and y0 <= left_player_coords[3]):
        # Ball hits the left player, check if it's on top or bottom part
        if y0 < left_player_coords[1] + player_height and y1 > left_player_coords[1]:
            # Ball is contacting top or bottom part of the player
            if y0 < left_player_coords[1] or y1 > left_player_coords[3]:
                reset_game()
            else:
                dx = -dx
    
    # Check for collision with right player
    right_player_coords = canvas.coords(right_player)
    if (x1 >= right_player_coords[0] and x0 <= right_player_coords[2]) and (y1 >= right_player_coords[1] and y0 <= right_player_coords[3]):
        # Ball hits the right player, check if it's on top or bottom part
        if y0 < right_player_coords[1] + player_height and y1 > right_player_coords[1]:
            # Ball is contacting top or bottom part of the player
            if y0 < right_player_coords[1] or y1 > right_player_coords[3]:
                reset_game()
            else:
                dx = -dx
    
    # Bounce off the walls
    if x0 <= 0 or x1 >= width:
        reset_game()
    if y0 <= 0 or y1 >= height:
        dy = -dy
    
    # Schedule the ball to move again after 20 ms
    root.after(20, move_ball)

def move_player(player, direction):
    coords = canvas.coords(player)
    if direction == "up" and coords[1] > 0:
        canvas.move(player, 0, -player_speed)
    elif direction == "down" and coords[3] < height:
        canvas.move(player, 0, player_speed)

# def key_press(event):
#     if event.keysym == "w":
#         move_player(left_player, "up")
#     elif event.keysym == "s":
#         move_player(left_player, "down")
#     elif event.keysym == "Up":
#         move_player(right_player, "up")
#     elif event.keysym == "Down":
#         move_player(right_player, "down")

root.geometry(f"{width}x{height}")


def key_up(e) :
    if  e.keycode in key_history :
        key_history.pop(key_history.index(e.keycode))

def key_down(e):
    if e.keycode not in key_history:
        key_history.append(e.keycode)
        if e.keysym == "w" :
            move_player(left_player, "up")
        elif e.keysym == "s" :
            move_player(left_player, "down")
        elif e.keysym == "Up" :
            move_player(right_player, "up")
        elif e.keysym == "Down" :
            move_player(right_player, "down")



# Bind key press events
root.bind("<KeyPress>", key_down)
root.bind("<KeyRelease>", key_up)

# Start the ball movement
move_ball()

root.mainloop()
