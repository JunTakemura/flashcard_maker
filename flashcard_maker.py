import tkinter as tk
from tkinter import filedialog, messagebox
import re
import sys
import os
import logging

# Constants configuration
MAX_FILE_SIZE = 1024 * 1024  # 1MB limit
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
FONT_SIZE = 50
FONT_NAME = "Arial"
ALLOWED_EXTENSIONS = ['.txt']

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')

class FlashcardApp:
    def __init__(self):
        self.words = []
        self.word_index = 0
        self.root = tk.Tk()
        self.setup_gui()

    def read_words(self, file_path):
        try:
            # Check file extension
            if not any(file_path.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS):
                logging.error("Invalid file type. Only .txt files are allowed.")
                messagebox.showerror("Error", "Invalid file type. Only .txt files are allowed.")
                sys.exit(1)

            # Check file size
            if os.path.getsize(file_path) > MAX_FILE_SIZE:
                logging.error("File size exceeds the maximum limit of 1MB.")
                messagebox.showerror("Error", "File size exceeds the maximum limit of 1MB.")
                sys.exit(1)

            with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                content = file.read()
                # Remove numbers, periods, and whitespace
                words = [re.sub(r'^\d+\.\s*', '', line.strip()) for line in content.splitlines()]
            return words

        except FileNotFoundError:
            logging.error(f"File '{file_path}' not found.")
            messagebox.showerror("Error", f"File '{file_path}' not found.")
            sys.exit(1)
        except PermissionError:
            logging.error(f"Permission denied when accessing '{file_path}'.")
            messagebox.showerror("Error", f"Permission denied when accessing '{file_path}'.")
            sys.exit(1)
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            sys.exit(1)

    def setup_gui(self):
        self.root.title("Flashcards")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        # Create a label to display the words
        self.label = tk.Label(self.root, text="", font=(FONT_NAME, FONT_SIZE), wraplength=WINDOW_WIDTH)
        self.label.pack(expand=True)

        # Bind specific keys to show next word
        self.root.bind("<space>", self.show_next_word)
        self.root.bind("<Right>", self.show_next_word)
        self.root.bind("<Return>", self.show_next_word)

        # Start by loading the words
        self.load_words()

    def load_words(self):
        # Open a file dialog to select the file
        file_name = filedialog.askopenfilename(title="Select the words file")
        if not file_name:
            logging.error("No file selected.")
            messagebox.showerror("Error", "No file selected.")
            sys.exit(1)

        # Load words from the file
        self.words = self.read_words(file_name)
        if not self.words:
            logging.error("The file is empty or contains invalid content.")
            messagebox.showerror("Error", "The file is empty or contains invalid content.")
            sys.exit(1)

        # Show the first word
        self.show_next_word()

    def show_next_word(self, event=None):
        if self.word_index < len(self.words):
            self.label.config(text=self.words[self.word_index])
            self.word_index += 1
        else:
            self.label.config(text="End of list")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = FlashcardApp()
    app.run()
