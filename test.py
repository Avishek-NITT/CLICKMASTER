import tkinter as tk
import random

height = 700
width = 700

# Initialize the click counter
click_counter = 0
# Dictionary to keep track of ovals and their removal times
oval_removal_timers = {}

def update_counter():
    global click_counter
    click_counter += 1
    counter_label.config(text=f"Clicks: {click_counter}")

def remove_oval(oval_id):
    # Remove the oval from the canvas
    if oval_id in oval_removal_timers:
        canvas.delete(oval_id)
        oval_removal_timers.pop(oval_id)

def create_oval():
    # Generate random coordinates and size for the circle
    x1 = random.randint(0, width - 100)
    y1 = random.randint(0, height - 100)
    radius = random.randint(20, 50)
    x2 = x1 + radius
    y2 = y1 + radius

    # Create a circle (an oval in Tkinter) on the canvas
    oval_id = canvas.create_oval(x1, y1, x2, y2, fill="lightblue", outline="blue")

    # Bind left mouse click event to the oval
    canvas.tag_bind(oval_id, "<Button-1>", lambda e: on_oval_click(oval_id))

    # Schedule automatic removal if not clicked within 1 second
    removal_timer = root.after(1100, lambda: remove_oval(oval_id))
    oval_removal_timers[oval_id] = removal_timer

def on_oval_click(oval_id):
    remove_oval(oval_id)
    update_counter()
    if oval_id in oval_removal_timers:
        root.after_cancel(oval_removal_timers.pop(oval_id))

# Initialize the main window
root = tk.Tk()
root.geometry(f"{width}x{height}")

# Create a label to show the click counter and pack it at the top
counter_label = tk.Label(root, text="Clicks: 0", font=("Arial", 20))
counter_label.pack(side="top", fill="x")

# Create a canvas with specified width and height
canvas = tk.Canvas(root, width=width, height=0.9*height, bg="white")
canvas.pack(side="bottom", fill="both", expand=True)

# Function to start spawning circles at intervals
def spawn_circle():
    create_oval()
    root.after(800, spawn_circle)

# Start spawning circles at intervals
spawn_circle()

# Start the Tkinter event loop
root.mainloop()
