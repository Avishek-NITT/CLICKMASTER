import tkinter as tk
import random

height = 700
width = 700

# Initialize the click counter and oval timers
click_counter = 0
oval_removal_timers = {}

def update_counter():
    global click_counter
    click_counter += 1
    counter_label.config(text=f"Clicks: {click_counter}")

def remove_oval(oval_id):
    # Remove the oval from the canvas
    canvas.delete(oval_id)
    if oval_id in oval_removal_timers:
        root.after_cancel(oval_removal_timers.pop(oval_id))

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
    removal_timer = root.after(1000, lambda: remove_oval(oval_id))
    oval_removal_timers[oval_id] = removal_timer

def on_oval_click(oval_id):
    update_counter()
    if oval_id in oval_removal_timers:
        root.after_cancel(oval_removal_timers.pop(oval_id))
    remove_oval(oval_id)

def reset():
    global click_counter
    click_counter = 0
    counter_label.config(text="Clicks: 0")
    
    # Clear all ovals from the canvas and cancel all timers
    canvas.delete("all")
    for timer in oval_removal_timers.values():
        root.after_cancel(timer)
    oval_removal_timers.clear()

def spawn_circle():
    create_oval()
    root.after(1000, spawn_circle)

# Initialize the main window
root = tk.Tk()
root.geometry(f"{width}x{height}")

# Create a frame to hold the counter label and reset button
frame = tk.Frame(root, width=width, bg="lightgray")
frame.pack(side="top")  # Ensure the frame is visible and fills horizontally

# Create a label to show the click counter and add it to the frame
counter_label = tk.Label(frame, text="Clicks: 0", font=("Arial", 20))
counter_label.pack(side="left", padx=10)

# Create a reset button and add it to the frame
reset_button = tk.Button(frame, text="Reset", font=("Arial", 20), command=reset)
reset_button.pack(side="right", padx=10)

# Create a canvas with specified width and height
canvas = tk.Canvas(root, width=width, height=0.9*height, bg="white")
canvas.pack(side="bottom", fill="both", expand=True)

# Start spawning circles at intervals
spawn_circle()

# Start the Tkinter event loop
root.mainloop()
