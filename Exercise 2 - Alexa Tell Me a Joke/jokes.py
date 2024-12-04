import tkinter as tk  # Import tkinter for the window
from tkinter import ttk  # Import ttk for themed widgets
import random  # Import random for selecting jokes
import os  # Import os for file handling

# Set up the main window
root = tk.Tk()
root.title("Alexa Tell Me A Joke!")
root.geometry("700x600")
root.configure(bg="#ffee66")  # Set background color

# Load jokes from a text file
def load_jokes(file_path):
    if not os.path.isfile(file_path):  # Check if file exists
        return []  # Return empty list if file is not found
    with open(file_path, 'r') as file:  # Open file in read mode
        return [joke.strip() for joke in file.readlines()]  # Read and clean up each line

# Display a random joke setup
def tell_joke():
    joke = random.choice(jokes)  # Choose a random joke
    setup, tell_joke.punchline = joke.split("?", 1)  # Split into setup and punchline
    joke_text.delete(1.0, tk.END)  # Clear text area
    joke_text.insert(tk.END, "" + setup + "? ")  # Show setup part with sparkle decor
    punchline_button.config(state="normal")  # Enable punchline button 

# Show the punchline of the joke
def show_punchline():
    joke_text.insert(tk.END, "\n\n " + tell_joke.punchline.strip() + " 😂")  # Add punchline with stars
    punchline_button.config(state="disabled")  # Disable punchline button 

# Set up the user interface
def setup_ui():
    # Main frame for the content
    frame = tk.Frame(root, bg="#ffee66")
    frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True) 

    # Title label
    title_label = tk.Label(
        frame, 
        text="Alexa Tell Me a Joke!", 
        bg="#ffee66", 
        fg="#ff66c4", 
        font=("Comic Sans MS", 28, "bold")
    )
    title_label.pack(pady=(10, 20))

    # Text area for displaying joke setup and punchline
    global joke_text
    joke_text = tk.Text(
        frame, 
        height=8, 
        width=50, 
        wrap=tk.WORD, 
        bg="#ffffff", 
        fg="#6677ff", 
        font=("Roboto", 14), 
        bd=0, 
        relief=tk.FLAT
    )
    joke_text.pack(pady=10)
    joke_text.config(
        highlightthickness=3, 
        highlightbackground="#6677ff", 
        highlightcolor="#6677ff"
    )

    # Button to display a new joke
    tell_joke_button = ttk.Button(frame, text="Tell me a Joke!", command=tell_joke)
    tell_joke_button.pack(pady=5, fill=tk.X)
    style_button(tell_joke_button)

    # Button to show the punchline (starts as disabled)
    global punchline_button
    punchline_button = ttk.Button(frame, text="Show Punchline", state="disabled", command=show_punchline)
    punchline_button.pack(pady=5, fill=tk.X)
    style_button(punchline_button)

    # Quit button to close the app
    quit_button = ttk.Button(frame, text="Quit", command=root.quit)
    quit_button.pack(pady=(10, 20), fill=tk.X)
    style_button(quit_button)

# Style for buttons
def style_button(button):
    button.config(style="TButton")  # Apply custom style
    style = ttk.Style()
    style.configure(
        "TButton", 
        font=("Roboto", 16, "bold"), 
        padding=10, 
        borderwidth=0
    )  # Style details
    style.map(
        "TButton", 
        foreground=[("active", "#6677ff")], 
        background=[("active", "#6677ff")]
    )

# Load jokes from the specified file path
jokes_file = 'Codelab Exercises/Exercise 2 - Alexa Tell Me a Joke/randomJokes.txt'
jokes = load_jokes(jokes_file)

setup_ui()  # Call setup to initialize the UI

root.mainloop()  # Run the main event loop
