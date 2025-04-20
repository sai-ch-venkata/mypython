from tkinter import *
from tkinter import messagebox, simpledialog, Toplevel
from PIL import Image, ImageDraw, ImageFont, ImageTk
import nltk
from textblob import TextBlob
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import random
import pygame
import time 

def play_bg():
    pygame.mixer.init()
    pygame.mixer.music.load(r"C:\Users\Administrator\python\corporate-background-music-314202.mp3")  # Replace with your file path
    pygame.mixer.music.play(-1)

def stop_bg():
    pygame.mixer.music.stop()

def play_win():
    pygame.mixer.init()
    pygame.mixer.music.load(r"C:\Users\Administrator\python\spinner-winner-287709.mp3")  # Replace with your file path
    pygame.mixer.music.play(1)

def stop_win():
    pygame.mixer.music.stop()

def play_pc():
    pygame.mixer.init()
    pygame.mixer.music.load(r"C:\Users\Administrator\python\participation-310011.mp3")  # Replace with your file path
    pygame.mixer.music.play(1)


def stop_pc():
    pygame.mixer.music.stop()



# Download NLTK resources with exception handling
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Passage Based Quiz")
        self.root.geometry("1000x800")

        self.logo = PhotoImage(file="sj_logo.png")  # Add logo

        # First canvas with borders and logo
        self.canvas1 = Canvas(root, width=1000, height=150, bg="white", highlightthickness=5, highlightbackground="gold")
        self.canvas1.pack(pady=10)
        self.canvas1.create_image(50, 50, anchor=NW, image=self.logo)
        self.canvas1.create_text(500, 50, text="Passage Based Quiz", font=("Arial", 30, "bold"), fill="blue")

        # Name entry
        self.name_label = Label(root, text="Enter Your Name:", font=("Arial", 20))
        self.name_label.pack(pady=10)
        self.name_entry = Entry(root, font=("Arial", 16), width=40)
        self.name_entry.pack(pady=10)

        # Passage frame with borders
        self.passage_frame = Frame(root, bd=5, relief=GROOVE, bg="white")
        self.passage_frame.pack(pady=20, padx=20, fill=BOTH, expand=True)
        self.passage_label = Label(self.passage_frame, text="Enter Passage:", font=("Arial", 20), bg="white")
        self.passage_label.pack(pady=10)
        self.passage_entry = Text(self.passage_frame, font=("Arial", 14), height=10, width=150, bg="white")
        self.passage_entry.pack(pady=20, padx=20, expand=True)

        # Start button
        self.start_button = Button(root, text="Start Quiz", font=("Arial", 16), command=self.start_quiz)
        self.start_button.pack(pady=10)

        # Quiz Frame
        self.quiz_frame = Frame(root)
        self.quiz_frame.pack(pady=20)
        self.question_label = Label(self.quiz_frame, font=("Arial", 14), wraplength=900, anchor='w')
        self.question_label.pack(pady=10)
        self.answer_entry = Entry(self.quiz_frame, font=("Arial", 14), width=80)
        self.answer_entry.pack(pady=10)

        # Submit button
        self.submit_button = Button(root, text="Submit Answer", font=("Arial", 16), command=self.submit_answer)
        self.submit_button.pack(pady=20)

        # Score label
        self.score_label = Label(root, text="Score: 0", font=("Arial", 20))
        self.score_label.pack(pady=10)

        self.questions = []
        self.current_index = 0
        self.score = 0

    def generate_quiz(self, text):

        blob = TextBlob(text)
        sentences = sent_tokenize(text)
        stop_words = set(stopwords.words('english'))

        quiz_questions = []
        for sentence in sentences:
            words = word_tokenize(sentence)
            words = [word for word in words if word.isalnum() and word.lower() not in stop_words]
            if words:
                word_to_remove = random.choice(words)
                question = sentence.replace(word_to_remove, "_____")
                quiz_questions.append((question, word_to_remove))

        return quiz_questions

    def start_quiz(self):
        text = self.passage_entry.get("1.0", END).strip()
        if not text:
            messagebox.showerror("Error", "Please enter a passage")
            return

        self.questions = self.generate_quiz(text)
        self.current_index = 0
        self.score = 0

        self.show_question()
        play_bg()

    def show_question(self):
        if self.current_index < len(self.questions):
            question, _ = self.questions[self.current_index]
            self.question_label.config(text=f"Q{self.current_index + 1}: {question}")
            self.answer_entry.delete(0, END)
        else:
            self.generate_certificate()

    def submit_answer(self):
        if self.current_index < len(self.questions):
            _, correct_answer = self.questions[self.current_index]
            user_answer = self.answer_entry.get().strip().lower()
            if user_answer == correct_answer.lower():
                self.score += 1
            self.score_label.config(text=f"Score: {self.score}")

            self.current_index += 1
            self.show_question()

    def get_medal_image(self):
        if self.score >= len(self.questions) * 0.8:
            return "gold_medal.png"
        elif self.score >= len(self.questions) * 0.5:
            return "silver_medal.jpeg"
        elif self.score >= len(self.questions) * 0.3:
            return "bronze_medal.jpeg"
        else:
            return "paticipation.jpeg"

    def generate_certificate(self):
        name = self.name_entry.get().strip()

        if not name:
            messagebox.showerror("Error", "Name is required to generate certificate")
            return

        cert = Image.new('RGB', (800, 600), color=(255, 255, 255))
        draw = ImageDraw.Draw(cert)

        # Add decorative border
        draw.rectangle([(20, 20), (780, 580)], outline="blue", width=15)
        draw.rectangle([(40, 40), (760, 560)], outline="gold", width=5)

        # Use a more stylish font
        title_font = ImageFont.truetype("arial.ttf", 50)
        text_font = ImageFont.truetype("arial.ttf", 40)

        # Add certificate text
        draw.text((200, 100), "Certificate of Achievement", fill="black", font=title_font)
        draw.text((200, 250), f"Presented to: {name}", fill="black", font=text_font)
        draw.text((200, 350), f"Score: {self.score}/{len(self.questions)}", fill="black", font=text_font)
        draw.text((200, 500), "Conducted by SJ Tournaments", fill="black", font=text_font)

        # Medal image
        medal_image = Image.open(self.get_medal_image()).resize((100, 100))
        cert.paste(medal_image, (350, 400))

        # Save the certificate
        cert.save("certificate.png")
        self.show_certificate()

    def show_certificate(self):
        cert_window = Toplevel(self.root)
        cert_window.title("Certificate")
        cert_window.geometry("800x600")

        canvas = Canvas(cert_window, width=800, height=600)
        canvas.pack()

        cert_image = Image.open("certificate.png")
        self.cert_tk_image = ImageTk.PhotoImage(cert_image)
        canvas.create_image(400, 300, anchor=CENTER, image=self.cert_tk_image)
        play_win()

if __name__ == "__main__":
    root = Tk()
    app = QuizApp(root)
    root.mainloop()
