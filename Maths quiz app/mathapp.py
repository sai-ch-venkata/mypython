import tkinter as tk
from tkinter import PhotoImage, messagebox
from PIL import Image, ImageTk
import random
import pygame

def play_bg():
    pygame.mixer.init()
    pygame.mixer.music.load(r"C:\Users\Administrator\python\corporate-background-music-314202.mp3")  # Replace with your file path
    pygame.mixer.music.play(-1)

def play_win():
    pygame.mixer.init()
    pygame.mixer.music.load(r"C:\Users\Administrator\python\spinner-winner-287709.mp3")  # Replace with your file path
    pygame.mixer.music.play(1)


# Create main window
root = tk.Tk()
root.title("Math Quiz App")
root.geometry("500x400")

# Load Image for Canvas Background
image_path = r"C:\Users\Administrator\python\logo.png"  # Replace with your path
bg_image = Image.open(image_path)
bg_image = bg_image.resize((50, 40))#esize to match window
bg_photo = ImageTk.PhotoImage(bg_image)  # Convert for Tkinter

# Create Canvas
canvas = tk.Canvas(root, width=500, height=400)
canvas.pack(fill="both", expand=True)

# Place Image on Canvas
canvas.create_image(10,0, anchor="nw", image=bg_photo)

# Variables
score = 0
question_count = 0
total_questions = random.randint(10, 50)-20
user_name = ""

# Function to start the quiz
def start_quiz():
    global user_name, score, question_count
    user_name = entry_name.get().strip()

    if not user_name:
        messagebox.showerror("Error", "Please enter your name!")
        return

    # Hide the name entry screen
    canvas.delete("all")  # Remove previous items
    canvas.create_image(0, 0, anchor="nw", image=bg_photo)  # Restore background

    # Show Quiz UI
    quiz_frame.place(relx=0.5, rely=0.5, anchor="center")
    generate_question()
    play_bg()

# Function to generate a random math question
def generate_question():
    global a, b, correct_answer, operator, question_count

    if question_count < total_questions:
        question_count += 1
        a, b = random.randint(1, 10), random.randint(1, 10)
        operator = random.choice(["+", "x"])

        correct_answer = a + b if operator == "+" else a * b
        lbl_question.config(text=f"Q{question_count}: {a} {operator} {b} = ?")
        entry_answer.delete(0, tk.END)
    else:
        show_certificate()

# Function to check the user's answer
def check_answer():
    global score
    user_answer = entry_answer.get().strip()

    if not user_answer.isdigit():
        messagebox.showwarning("Warning", "Please enter a valid number!")
        return

    score += 1 if int(user_answer) == correct_answer else -1
    generate_question()

# Function to display the participation certificate
def show_certificate():
    global bg_photo1  # Make the image global so it persists

    quiz_frame.place_forget()

    cert_window = tk.Toplevel(root)
    cert_window.title("Certificate of Participation")
    cert_window.geometry("600x400")

    # Certificate Content
    tk.Label(cert_window, text="Certificate of Participation", font=("Arial", 20, "bold")).pack(pady=10)
    tk.Label(cert_window, text=f"This is proudly presented to {user_name}", font=("Arial", 14)).pack(pady=5)
    tk.Label(cert_window, text=f"Final Score: {score}/{total_questions}", font=("Arial", 12)).pack(pady=15)
    tk.Button(cert_window, text="Close", font=("Arial", 12), command=cert_window.destroy).pack(pady=20)

    # Load Image and Keep Reference
    image_path = r"C:\Users\Administrator\python\logo.png"  # Replace with your path
    bg_image1 = Image.open(image_path)
    bg_image1 = bg_image1.resize((100, 100))  # Resize the image
    bg_photo1 = ImageTk.PhotoImage(bg_image1)  # Store globally

    # Display Logo on Certificate Window
    logo_label = tk.Label(cert_window, image=bg_photo1)
    logo_label.pack(pady=10)

    play_win()

# ------------------- GUI Layout -------------------

# Entry for participant name
lbl_name = tk.Label(root, text="Enter Your Name:", font=("Arial", 14), bg="lightblue")
canvas.create_window(250, 100, window=lbl_name)

entry_name = tk.Entry(root, font=("Arial", 12), width=30)
canvas.create_window(250, 130, window=entry_name)

btn_start = tk.Button(root, text="Start Quiz", font=("Arial", 12), command=start_quiz)
canvas.create_window(250, 170, window=btn_start)

# Quiz UI (Initially hidden)
quiz_frame = tk.Frame(root, bg="lightblue")

lbl_question = tk.Label(quiz_frame, text="", font=("Arial", 16), bg="lightblue")
lbl_question.pack(pady=10)

entry_answer = tk.Entry(quiz_frame, font=("Arial", 14), width=10)
entry_answer.pack(pady=5)

btn_submit = tk.Button(quiz_frame, text="Submit Answer", font=("Arial", 12), command=check_answer)
btn_submit.pack(pady=10)

quiz_frame.place_forget()

# Run the application
root.mainloop()
