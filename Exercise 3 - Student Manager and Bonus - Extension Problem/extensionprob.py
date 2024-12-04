import tkinter as tk
from tkinter import ttk, messagebox # Import ttk for themed widgets
import os # Import os for file handling

root = tk.Tk()
root.title("Student Manager")
root.geometry("600x800")
root.configure(bg="#fff8e7")  

# Load student data from a file
def load_student_data(file_path): 
    if not os.path.isfile(file_path):
        return []
    with open(file_path, 'r') as file:
        data = file.readlines()
    students = []
    for line in data[1:]:  
        parts = line.strip().split(',')
        if len(parts) < 6: 
            print(f"Skipping invalid line: {line}")  
            continue  
        student_number = parts[0]
        name = parts[1]
        
        try:
            coursework_marks = list(map(float, parts[2:5])) 
        except ValueError as e:
            print(f"Error processing coursework marks for {name}: {e}") 
            continue
        
        try:
            exam_mark = float(parts[5]) 
        except ValueError:
            print(f"Invalid exam mark for {name}. Expected a number, got {parts[5]}")
            exam_mark = 0  
        
        total_coursework = sum(coursework_marks) # Sum coursework marks
        total_marks = total_coursework + exam_mark # Calculate total marks
        percentage = (total_marks / 160) * 100 # Calculate percentage
        grade = calculate_grade(percentage) # Calculate grade
        students.append((student_number, name, total_coursework, exam_mark, percentage, grade)) # Add student to list
    return students

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

# Display all student records
def display_student_records():
    output_text.delete(1.0, tk.END)
    for student in students:
        output_text.insert(tk.END, format_student(student)) # Display formatted student data
    avg_percentage = sum(student[4] for student in students) / len(students) if students else 0 # Calculate average percentage
    output_text.insert(tk.END, f"Number of Students: {len(students)}\n") 
    output_text.insert(tk.END, f"Average Percentage: {avg_percentage:.2f}%\n")

# Format student data
def format_student(student):
    return (f"Name: {student[1]}\n"
            f"Student Number: {student[0]}\n"
            f"Total Coursework Mark: {student[2]}\n"
            f"Exam Mark: {student[3]}\n"
            f"Overall Percentage: {student[4]:.2f}%\n"
            f"Grade: {student[5]}\n\n")

# Display the student with the highest score
def show_highest_score():
    highest_student = max(students, key=lambda s: s[4])
    display_student(highest_student)

# Display the student with the lowest score
def show_lowest_score():
    lowest_student = min(students, key=lambda s: s[4])
    display_student(lowest_student)

# Display a single student's record
def display_student(student):
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, format_student(student))

# Add a new student record
def add_student_record():
    student_number = student_number_entry.get()
    name = name_entry.get()
    coursework1 = int(coursework1_entry.get())
    coursework2 = int(coursework2_entry.get())
    coursework3 = int(coursework3_entry.get())
    exam_mark = int(exam_mark_entry.get())
    total_coursework = coursework1 + coursework2 + coursework3
    total_marks = total_coursework + exam_mark
    percentage = (total_marks / 160) * 100
    grade = calculate_grade(percentage)
    new_student = (student_number, name, total_coursework, exam_mark, percentage, grade)
    students.append(new_student)
    save_to_file()
    update_student_dropdown()
    messagebox.showinfo("Success", "Student record added!")

#  Delete a student record
def delete_student_record():
    selected_student = student_dropdown.get() # Get selected student
    global students
    students = [s for s in students if s[1] != selected_student] # Remove selected student
    save_to_file()
    update_student_dropdown()
    messagebox.showinfo("Success", "Student record deleted!")

# Update a student record
def update_student_record(): # Update a student record
    selected_student = student_dropdown.get()
    student_index = next((i for i, s in enumerate(students) if s[1] == selected_student), None) # Get index of selected student
    
    if student_index is not None: # Check if student is found
        field_to_update = field_var.get() # Get field to update
        if field_to_update == "Name":
            students[student_index] = (students[student_index][0], name_entry.get(), students[student_index][2], # Update name
                                        students[student_index][3], students[student_index][4], students[student_index][5]) # Update other fields
        elif field_to_update == "Total Coursework": # Update total coursework
            coursework1 = int(coursework1_entry.get())
            coursework2 = int(coursework2_entry.get())
            coursework3 = int(coursework3_entry.get())
            total_coursework = coursework1 + coursework2 + coursework3
            students[student_index] = (students[student_index][0], students[student_index][1],
                                        total_coursework, students[student_index][3], 
                                        students[student_index][4], students[student_index][5])
        elif field_to_update == "Exam Mark": # Update exam mark
            students[student_index] = (students[student_index][0], students[student_index][1],
                                        students[student_index][2], int(exam_mark_entry.get()), 
                                        students[student_index][4], students[student_index][5])
        save_to_file() 
        update_student_dropdown()
        messagebox.showinfo("Success", "Student record updated!")

# Save student data to file
def save_to_file():
    with open('Codelab Exercises/Exercise 3 - Student Manager and Bonus - Extension Problem/studentMarks.txt', 'w') as file:
        file.write("Student Number,Name,Coursework1,Coursework2,Coursework3,Exam Mark\n")
        for student in students:
            file.write(f"{student[0]},{student[1]},{student[2]},{student[3]},{student[4]},{student[5]}\n") # Write student data to file

# Sort student records
order_var = tk.StringVar(value="Ascending")

tk.Label(root, text="Sort Order", font=("Times New Roman", 14), bg="#fff8e7").pack(pady=5) 
sort_order_options = ["Ascending", "Descending"]
for option in sort_order_options: 
    ttk.Radiobutton(root, text=option, variable=order_var, value=option).pack(pady=2)
def sort_student_records():
    order = order_var.get()
    if order == "Ascending":
        sorted_students = sorted(students, key=lambda s: s[4])
    else:
        sorted_students = sorted(students, key=lambda s: s[4], reverse=True)
    output_text.delete(1.0, tk.END)
    for student in sorted_students:
        output_text.insert(tk.END, format_student(student))

# Update student dropdown
def update_student_dropdown():
    student_dropdown['values'] = [student[1] for student in students] # Update student dropdown

header_label = tk.Label(root, text="Student Record's Manager", font=("Times New Roman", 18, "bold"), bg="#fff8e7")  
header_label.pack(pady=10)

menu_frame = tk.Frame(root, bg="#fff8e7")  
menu_frame.pack(pady=10)

# Create buttons
buttons = [
    ("Display All Records", display_student_records),
    ("Show Highest Score", show_highest_score),
    ("Show Lowest Score", show_lowest_score),
    ("Sort Records", sort_student_records),
    ("Add Student Record", add_student_record),
    ("Delete Student Record", delete_student_record),
    ("Update Student Record", update_student_record),
]

for i, (text, command) in enumerate(buttons): 
    button = tk.Button(menu_frame, text=text, command=command, bg="#fdb9b4", font=("Roboto", 12), width=18)  
    button.grid(row=i // 3, column=i % 3, padx=5, pady=5, sticky="ew")
# Create a frame for the form
form_frame = tk.Frame(root, bg="#fff8e7")  #
form_frame.pack(pady=10)

# Create form elements
tk.Label(form_frame, text="Student Number", bg="#a8d64c", font=("Roboto", 12)).grid(row=0, column=0, padx=5, pady=5, sticky='e')
student_number_entry = tk.Entry(form_frame, font=("Roboto", 12))
student_number_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(form_frame, text="Name", bg="#a8d64c", font=("Roboto", 12)).grid(row=1, column=0, padx=5, pady=5, sticky='e')
name_entry = tk.Entry(form_frame, font=("Roboto", 12))
name_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(form_frame, bg="#a8d64c", text="Coursework Mark 1", font=("Roboto", 12)).grid(row=2, column=0, padx=5, pady=5, sticky='e')
coursework1_entry = tk.Entry(form_frame, font=("Roboto", 12))
coursework1_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(form_frame, bg="#a8d64c", text="Coursework Mark 2", font=("Roboto", 12)).grid(row=3, column=0, padx=5, pady=5, sticky='e')
coursework2_entry = tk.Entry(form_frame, font=("Roboto", 12))
coursework2_entry.grid(row=3, column=1, padx=5, pady=5)

tk.Label(form_frame, bg="#a8d64c", text="Coursework Mark 3", font=("Roboto", 12)).grid(row=4, column=0, padx=5, pady=5, sticky='e')
coursework3_entry = tk.Entry(form_frame, font=("Roboto", 12))
coursework3_entry.grid(row=4, column=1, padx=5, pady=5)

tk.Label(form_frame, bg="#a8d64c", text="Exam Mark", font=("Roboto", 12)).grid(row=5, column=0, padx=5, pady=5, sticky='e')
exam_mark_entry = tk.Entry(form_frame, font=("Roboto", 12))
exam_mark_entry.grid(row=5, column=1, padx=5, pady=5)

field_var = tk.StringVar(value="Name")
tk.Label(root, text="Field to Update", font=("Times New Roman", 14), bg="#fff8e7").pack(pady=5)  
field_options = ["Name", "Total Coursework", "Exam Mark"]
for option in field_options:
    ttk.Radiobutton(root, text=option, variable=field_var, value=option).pack(pady=2)

student_dropdown = ttk.Combobox(root, values=[], state="readonly", font=("Roboto", 12))
student_dropdown.pack(pady=10)

output_frame = tk.Frame(root)
output_frame.pack(pady=5, fill=tk.BOTH, expand=True)

output_text = tk.Text(output_frame, height=15, bg="#a8d64c", wrap=tk.WORD, font=("Roboto", 12))  
output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(output_frame, command=output_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
output_text.config(yscrollcommand=scrollbar.set)

students = load_student_data('Codelab Exercises/Exercise 3 - Student Manager and Bonus - Extension Problem/studentMarks.txt') # Load student data
update_student_dropdown()

root.mainloop()
