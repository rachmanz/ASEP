import numpy as np
import pandas as pd
import cv2
import os
import operator
from string import ascii_uppercase
from tkinter import filedialog
from PIL import Image, ImageTk
from tensorflow.keras.models import model_from_json
import customtkinter as ctk
from spellchecker import SpellChecker

# CUDA ACTIVATION MODE
os.environ['THEANO_FLAGS'] = "device=cuda, assert_no_cpu_op=True"

class Application(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sign Language To Text Conversion")
        self.geometry("900x900")

        self.vs = cv2.VideoCapture(0)
        self.current_image = None
        self.current_image2 = None
        self.json_file = open("../Sign-Hand-to-Text-Pipeline/Models/model_new_1.json", "r")
        self.model_json = self.json_file.read()
        self.json_file.close()

        self.loaded_model = model_from_json(self.model_json)
        self.loaded_model.load_weights("../Sign-Hand-to-Text-Pipeline/Models/model_new_2.h5")

        self.ct = {}
        self.ct['blank'] = 0
        self.blank_flag = 0

        for i in ascii_uppercase:
            self.ct[i] = 0

        print("Loaded model from disk")

        self.spell = SpellChecker()  # Create an instance of SpellChecker

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame = ctk.CTkFrame(self, width=900, height=900)
        self.frame.grid(row=0, column=1, sticky="nsew")

        self.panel = ctk.CTkLabel(self.frame)
        self.panel.grid(row=0, column=0, padx=10, pady=10)

        self.panel2 = ctk.CTkLabel(self.frame)
        self.panel2.grid(row=0, column=1, padx=10, pady=10)

        self.title_label = ctk.CTkLabel(self.frame, text="Sign Language To Text Conversion", font=ctk.CTkFont(size=30, weight="bold"))
        self.title_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.panel3 = ctk.CTkLabel(self.frame, text_color="white")
        self.panel3.grid(row=2, column=1, padx=10, pady=10)

        self.char_label = ctk.CTkLabel(self.frame, text="Character :", font=ctk.CTkFont(size=20, weight="bold"))
        self.char_label.grid(row=2, column=0, padx=10, pady=10)

        self.panel4 = ctk.CTkLabel(self.frame, text_color="white")
        self.panel4.grid(row=3, column=1, padx=10, pady=10)

        self.word_label = ctk.CTkLabel(self.frame, text="Word :", font=ctk.CTkFont(size=20, weight="bold"))
        self.word_label.grid(row=3, column=0, padx=10, pady=10)

        self.panel5 = ctk.CTkLabel(self.frame, text_color="white")
        self.panel5.grid(row=4, column=1, padx=10, pady=10)

        self.sentence_label = ctk.CTkLabel(self.frame, text="Sentence :", font=ctk.CTkFont(size=20, weight="bold"))
        self.sentence_label.grid(row=4, column=0, padx=10, pady=10)

        self.close_button = ctk.CTkButton(self.frame, text="Close", command=self.close_windows)
        self.close_button.grid(row=5, column=0, columnspan=2, pady=10)

        self.str = ""
        self.word = " "
        self.current_symbol = "Empty"
        self.photo = "Empty"
        self.video_loop()

    def video_loop(self):
        ok, frame = self.vs.read()

        if ok:
            cv2image = cv2.flip(frame, 1)

            x1 = int(0.5 * frame.shape[1])
            y1 = 10
            x2 = frame.shape[1] - 10
            y2 = int(0.5 * frame.shape[1])

            cv2.rectangle(frame, (x1 - 1, y1 - 1), (x2 + 1, y2 + 1), (255, 0, 0), 1)
            cv2image = cv2.cvtColor(cv2image, cv2.COLOR_BGR2RGBA)

            self.current_image = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=self.current_image)

            self.panel.configure(image=imgtk)
            self.panel.image = imgtk

            cv2image = cv2image[y1: y2, x1: x2]

            gray = cv2.cvtColor(cv2image, cv2.COLOR_BGR2GRAY)

            blur = cv2.GaussianBlur(gray, (5, 5), 2)

            th3 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

            ret, res = cv2.threshold(th3, 70, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

            self.predict(res)

            self.current_image2 = Image.fromarray(res)

            imgtk = ImageTk.PhotoImage(image=self.current_image2)

            self.panel2.configure(image=imgtk)
            self.panel2.image = imgtk

            self.panel3.configure(text=self.current_symbol, font=ctk.CTkFont(size=30), text_color="white")

            self.panel4.configure(text=self.word, font=ctk.CTkFont(size=30), text_color="white")

            self.panel5.configure(text=self.str, font=ctk.CTkFont(size=30), text_color="white")

        self.after(5, self.video_loop)

    def predict(self, test_image):
        test_image = cv2.resize(test_image, (128, 128))
        result = self.loaded_model.predict(test_image.reshape(1, 128, 128, 1))
        prediction = {}

        prediction['blank'] = result[0][0]
        inde = 1

        for i in ascii_uppercase:
            prediction[i] = result[0][inde]
            inde += 1

        prediction = sorted(prediction.items(), key=operator.itemgetter(1), reverse=True)
        self.current_symbol = prediction[0][0]

        self.ct[self.current_symbol] += 1

        if self.ct[self.current_symbol] > 60:
            for i in ascii_uppercase:
                if i == self.current_symbol:
                    continue
                tmp = self.ct[self.current_symbol] - self.ct[i]
                if tmp < 0:
                    tmp *= -1
                if tmp <= 20:
                    self.ct['blank'] = 0
                    for i in ascii_uppercase:
                        self.ct[i] = 0
                    return

            self.ct['blank'] = 0

            for i in ascii_uppercase:
                self.ct[i] = 0

            if self.current_symbol == 'blank':
                if self.blank_flag == 0:
                    self.blank_flag = 1

                    if len(self.str) > 0:
                        self.str += " "

                    self.str += self.word

                    self.word = ""
                    self.check_sentence()  # Call the check_sentence method
            else:
                if len(self.str) > 16:
                    self.str = ""
                    self.blank_flag = 0
                self.word += self.current_symbol

    def check_sentence(self):
        misspelled_words = self.spell.unknown(self.str.split())
        for word in misspelled_words:
            suggestions = self.spell.candidates(word)
            if suggestions:
                print(f"Misspelled word: {word}")
                print(f"Suggested corrections: {', '.join(suggestions[:3])}")

    def close_windows(self):
        self.destructor()
        self.destroy()

    def destructor(self):
        # Save the result data to a CSV file
        result_data = {
            'Character': [self.panel3.cget("text")],
            'Word': [self.panel4.cget("text")],
            'Sentence': [self.panel5.cget("text")]
        }
        result_df = pd.DataFrame(result_data)
        result_file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if result_file_path:
            result_df.to_csv(result_file_path, index=False)
            print(f"Result data saved to CSV file: {result_file_path}")

        # Release resources
        print("Closing Application...")
        self.vs.release()
        cv2.destroyAllWindows()

print("Starting Application...")
app = Application()
app.mainloop()