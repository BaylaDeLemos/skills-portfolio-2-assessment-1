import tkinter as tk  # For creating the GUI
from tkinter import ttk
from PIL import Image, ImageTk  # For handling images
import os  # Import os for file handling

# Initialize the main window
root = tk.Tk()
root.title("Student Manager")  # Set title of the window
root.geometry("500x600")  # Set size of the window
root.resizable(False, False)  # Disable resizing
    
# Load an image for the background
bg_image_path = "Codelab Exercises/Exercise 3 - Student Manager and Bonus - Extension Problem/Student manager.png"  # Replace with your image file path
if os.path.isfile(bg_image_path):
    bg_image = Image.open(bg_image_path)
    bg_image = bg_image.resize((500, 600), Image.Resampling.LANCZOS)  # Resize to fit the window
    bg_photo = ImageTk.PhotoImage(bg_image)
else:
    bg_photo = None

# Canvas for the background image
canvas = tk.Canvas(root, width=500, height=600)
canvas.pack(fill="both", expand=True)

if bg_photo:
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")  # Add background image

# Load student data from a file and calculate necessary information
def load_student_data(file_path):
    if not os.path.isfile(file_path):  # Check if file exists
        return []
    with open(file_path, 'r') as file:
        data = file.readlines()  # Read all lines
    students = []
    for line in data[1:]:  # Skip header line
        parts = line.strip().split(',')  # Split each line by commas
        student_number = parts[0]
        name = parts[1]
        coursework_marks = list(map(int, parts[2:5]))  # Convert coursework marks to integers
        exam_mark = int(parts[5])  # Convert exam mark to integer
        total_coursework = sum(coursework_marks)  # Sum coursework marks
        total_marks = total_coursework + exam_mark  # Calculate total marks
        percentage = (total_marks / 160) * 100  # Calculate percentage
        grade = calculate_grade(percentage)  # Calculate grade based on percentage
        students.append((student_number, name, total_coursework, exam_mark, percentage, grade))
    return students  # Return list of students with calculated data

# Determine grade based on percentage
def calculate_grade(percentage):
    if percentage >= 70:
        return 'A'
    elif percentage >= 60:
        return 'B'
    elif percentage >= 50:
        return 'C'
    elif percentage >= 40:
        return 'D'
    else:
        return 'F'

# Load student data from file
students = load_student_data('Codelab Exercises/Student Manager/studentMarks.txt')

# Display all student records in the text box
def display_student_records():
    output_text.delete(1.0, tk.END)  # Clear text box
    for student in students:
        output_text.insert(tk.END, f"Name: {student[1]}\n")
        output_text.insert(tk.END, f"Student Number: {student[0]}\n")
        output_text.insert(tk.END, f"Total Coursework Mark: {student[2]}\n")
        output_text.insert(tk.END, f"Exam Mark: {student[3]}\n")
        output_text.insert(tk.END, f"Overall Percentage: {student[4]:.2f}%\n")
        output_text.insert(tk.END, f"Grade: {student[5]}\n\n")
    avg_percentage = sum(student[4] for student in students) / len(students) if students else 0
    output_text.insert(tk.END, f"Number of Students: {len(students)}\n")
    output_text.insert(tk.END, f"Average Percentage: {avg_percentage:.2f}%\n")

# Display the student with the highest score
def show_highest_score():
    highest_student = max(students, key=lambda s: s[4])  # Find student with highest percentage
    display_student(highest_student)  # Display that student's data

# Display the student with the lowest score
def show_lowest_score():
    lowest_student = min(students, key=lambda s: s[4])  # Find student with lowest percentage
    display_student(lowest_student)  # Display that student's data

# Display a single student's record
def display_student(student):
    output_text.delete(1.0, tk.END)  # Clear text box
    output_text.insert(tk.END, f"Name: {student[1]}\n")
    output_text.insert(tk.END, f"Student Number: {student[0]}\n")
    output_text.insert(tk.END, f"Total Coursework Mark: {student[2]}\n")
    output_text.insert(tk.END, f"Exam Mark: {student[3]}\n")
    output_text.insert(tk.END, f"Overall Percentage: {student[4]:.2f}%\n")
    output_text.insert(tk.END, f"Grade: {student[5]}\n")

# Display the selected student's record from the dropdown
def view_selected_student():
    selected_index = student_dropdown.current()
    if selected_index != -1:
        display_student(students[selected_index])

# Load student data from file
students = load_student_data('Codelab Exercises/Exercise 3 - Student Manager and Bonus - Extension Problem/studentMarks.txt')

# Frame for action buttons
button_frame = tk.Frame(root, bg="#fff8e7")
button_frame_window = canvas.create_window(250, 80, window=button_frame)

# Button to view all student records
view_records_button = tk.Button(button_frame, text="View All Records", command=display_student_records, height=2, width=20, bg="#a8d64c", fg="white", font=("arial", 9, "bold"))
view_records_button.grid(row=0, column=0, padx=5)

# Button to view the student with the highest score
highest_score_button = tk.Button(button_frame, text="Highest Score", command=show_highest_score, height=2, width=20, bg="#a8d64c", fg="white", font=("arial", 9, "bold"))
highest_score_button.grid(row=0, column=1, padx=5)

# Button to view the student with the lowest score
lowest_score_button = tk.Button(button_frame, text="Lowest Score", command=show_lowest_score, height=2, width=20, bg="#a8d64c", fg="white", font=("arial", 9, "bold"))
lowest_score_button.grid(row=0, column=2, padx=5)

# Dropdown menu to select a student by name
student_dropdown = ttk.Combobox(root, values=[student[1] for student in students], state="readonly")
student_dropdown.place(x=70, y=160, width=200)  # Adjust x, y, and width as needed

# Button to view the selected student's record from the dropdown
view_selected_button = tk.Button(root, text="View Selected Student Record", command=view_selected_student, bg="#a8d64c", fg="white", font=("arial", 9, "bold"))
view_selected_button.place(x=280, y=159)  # Adjust x and y to position the button next to the dropdown

# Text box to display student records
output_text = tk.Text(root, height=20, width=60)
output_text_window = canvas.create_window(250, 360, window=output_text)

# Start the application
root.mainloop()
