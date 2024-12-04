import tkinter as tk
from tkinter import messagebox
import random

# Initialize the main window
root = tk.Tk()
root.title("Math Quiz Game")  # Set window title
root.geometry("500x500")  # Set window size
root.configure(bg="#ffe5b7")  # Set background color
root.resizable(False, False)  # Disable resizing of the window

# Initialize global variables
score = 0
current_question = 1
total_questions = 10
level = 1
num1 = 0
num2 = 0
operation = ""
correct_answer = 0

# Function to reset the game
def reset_game():
    global score, current_question
    score = 0
    current_question = 1
    update_score()  # Update the score label
    display_start_page()  # Show the start page

# Function to generate random numbers based on the level
def random_number(level):
    if level == 1:
        return random.randint(1, 10)  # Easy level: Random integer between 1 and 10
    elif level == 2:
        return round(random.uniform(1, 50), 2)  # Moderate level: Random float between 1 and 50
    elif level == 3:
        return round(random.uniform(1, 100), 2)  # Advanced level: Random float between 1 and 100

# Function to decide the operation based on the level
def decide_operation(level):
    if level == 1:
        return random.choice(['+', '-'])  # Easy level: Choose between addition and subtraction
    else:
        return random.choice(['+', '-', '*', '/'])  # Higher levels: Choose between addition, subtraction, multiplication, and division

# Function to update the score label
def update_score():
    score_label.config(text=f"Score: {score}")

# Function to display the next math problem
def display_problem():
    global num1, num2, operation, correct_answer, current_question, total_questions
    num1 = random_number(level)  # Generate first number
    num2 = random_number(level)  # Generate second number
    operation = decide_operation(level)  # Decide the operation to use
    if operation == '+':
        correct_answer = num1 + num2  # Correct answer for addition
    elif operation == '-':
        correct_answer = num1 - num2  # Correct answer for subtraction
    elif operation == '*':
        correct_answer = num1 * num2  # Correct answer for multiplication
    elif operation == '/':
        while num2 == 0:  # Ensure no division by zero
            num2 = random_number(level)
        correct_answer = num1 / num2  # Correct answer for division
    # Display the question and equation
    question_label.config(text=f"⭐ Question {current_question}/{total_questions} ⭐\n")
    equation_label.config(text=f"{num1} {operation} {num2} =")
    entry_answer.delete(0, tk.END)  # Clear the previous answer

# Function to check the user's answer
def check_answer():
    global score, current_question, correct_answer
    try:
        user_answer = float(entry_answer.get())  # Get the user's input as a float
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a number.")  # Show error if input is not a number
        return
    if abs(user_answer - correct_answer) < 0.01:  # Allow for slight floating-point differences
        score += 1  # Increment score if correct
        messagebox.showinfo("Correct!", "Good job!")  # Show message if the answer is correct
    else:
        messagebox.showinfo("Incorrect", f"The correct answer was {correct_answer:.2f}")  # Show the correct answer if the user is wrong
    update_score()  # Update the score label
    current_question += 1  # Move to the next question
    if current_question > total_questions:
        show_results()  # Show results if all questions have been answered
    else:
        display_problem()  # Otherwise, display the next problem

# Function to show the results after the quiz
def show_results():
    global score
    # Determine the rank based on the score
    if score == 10:
        rank = "A+ (Perfect!) ⭐⭐⭐⭐"
    elif score >= 8:
        rank = "A (Great Job!) ⭐⭐⭐"
    elif score >= 6:
        rank = "B (Good Effort!) ⭐⭐"
    elif score >= 4:
        rank = "C (You can do better!)"
    else:
        rank = "F (Try again!)"
    # Show the results in a messagebox
    messagebox.showinfo("Quiz Complete", f"Your score is: {score} out of 10\nRank: {rank}")
    reset_game()  # Reset the game after showing the results

# Function to start the quiz with the selected difficulty level
def start_quiz(selected_level):
    global level
    level = selected_level  # Set the chosen level
    levels_frame.pack_forget()  # Hide the levels selection frame
    quiz_frame.pack(pady=20)  # Show the quiz frame
    display_problem()  # Display the first question

# Function to display the start page
def display_start_page():
    quiz_frame.pack_forget()  # Hide the quiz frame
    start_page_frame.pack(pady=20)  # Show the start page

# Function to display the levels page
def display_levels_page():
    start_page_frame.pack_forget()  # Hide the start page
    levels_frame.pack(pady=20)  # Show the levels page

# Start page frame with instructions
start_page_frame = tk.Frame(root, bg="#ffe5b7")
start_label = tk.Label(start_page_frame, text="Math Quiz Game", font=("system", 20, "bold"), bg="#ffe5b7", fg="#8b1874")
start_label.pack(pady=20)
start_label = tk.Label(start_page_frame, text="Rules:\n\n1. Choose difficulty level.\n\n2. Answer as many questions as you can.\n\n3. Strive to get the highest score!", font=("Roboto", 14), bg="#ffe5b7", fg="#8b1874")
start_label.pack(pady=20)
start_button = tk.Button(start_page_frame, text="Start Game", font=("system", 17), command=display_levels_page, bg="#d34a24", fg="white", width=15)
start_button.pack(pady=10)

# Levels page frame
levels_frame = tk.Frame(root, bg="#ffe5b7")
levels_label = tk.Label(levels_frame, text="Choose Difficulty Level", font=("system", 20, "bold"), bg="#ffe5b7", fg="#b71375")
levels_label.pack(pady=20)

# Buttons to select difficulty level
easy_button = tk.Button(levels_frame, text="Easy", font=("system", 15), command=lambda: start_quiz(1), width=15, height=2, fg="white", bg="#f68b6d")
moderate_button = tk.Button(levels_frame, text="Moderate", font=("system", 15), command=lambda: start_quiz(2), width=15, height=2, fg="white", bg="#f69e04")
advanced_button = tk.Button(levels_frame, text="Advanced", font=("system", 15), command=lambda: start_quiz(3), width=15, height=2, fg="white", bg="#d34a24")

easy_button.pack(pady=5)
moderate_button.pack(pady=5)
advanced_button.pack(pady=5)

# Quiz frame where questions are displayed
quiz_frame = tk.Frame(root, bg="#ffe5b7")
question_label = tk.Label(quiz_frame, text="", font=("system", 16), bg="#ffe5b7", fg="#8b1874")
question_label.pack(pady=10)

equation_label = tk.Label(quiz_frame, text="", font=("system", 16), bg="#ffe5b7", fg="#8b1874")
equation_label.pack(pady=10)

entry_answer = tk.Entry(quiz_frame, font=("system", 14), bd=2, relief="groove", width=20)
entry_answer.pack(pady=10)

submit_button = tk.Button(quiz_frame, text="Submit Answer", font=("system", 15), command=check_answer, bg="#d34a24", fg="white")
submit_button.pack(pady=10)

score_label = tk.Label(quiz_frame, text="Score: 0", font=("System", 14), bg="#ffe5b7", fg="#d34a24")
score_label.pack(pady=10)

# Display the start page when the program runs
display_start_page()

# Run the main event loop
root.mainloop()