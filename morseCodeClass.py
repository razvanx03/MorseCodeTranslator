from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel
from morse.Morse import Morse
import pygame
import wave
import numpy as np

class MorseCodeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        pygame.mixer.init(frequency=44100, size=-16, channels=1)

    def initUI(self):
        self.setWindowTitle('Morse Code Converter')
        self.setStyleSheet("background-color: lightblue;")

        layout = QVBoxLayout()
        self.setFixedSize(500, 300)

        self.text_input = QLineEdit(self)
        self.text_input.setPlaceholderText("Enter text to convert to Morse")
        self.text_input.setText("Hello")
        self.text_input.setStyleSheet("background-color: lightgrey")
        layout.addWidget(self.text_input)

        self.morse_input = QLineEdit(self)
        self.morse_input.setPlaceholderText("Enter Morse code to decode")
        self.morse_input.setText(".-- --- .-. .-.. -..")
        self.morse_input.setStyleSheet("background-color: lightgrey")
        layout.addWidget(self.morse_input)


        self.convert_text_button = QPushButton('Convert to Morse', self)
        self.convert_text_button.clicked.connect(self.convert_text_to_morse)
        layout.addWidget(self.convert_text_button)

        self.convert_morse_button = QPushButton('Convert Morse to Text', self)
        self.convert_morse_button.clicked.connect(self.convert_morse_to_text)
        layout.addWidget(self.convert_morse_button)

        self.result_label_text = QLabel('Morse to Text: ', self)
        layout.addWidget(self.result_label_text)
        layout.setAlignment(self.result_label_text, Qt.AlignCenter)

        self.result_label_morse = QLabel('Text to Morse: ', self)
        layout.addWidget(self.result_label_morse)
        layout.setAlignment(self.result_label_morse, Qt.AlignCenter)

        self.play_sound_button = QPushButton('Play Morse Sound', self)
        self.play_sound_button.clicked.connect(self.play_morse_sound)
        layout.addWidget(self.play_sound_button)

        self.setLayout(layout)

        self.morse_code = None

    def convert_text_to_morse(self):
        morse = Morse()
        text = self.text_input.text()
        self.morse_code = morse.to_morse(text)
        self.result_label_morse.setText(f"Text to Morse: {self.morse_code}")

    def convert_morse_to_text(self):
        morse = Morse()
        self.text_code = self.morse_input.text()
        text = morse.to_string(self.text_code)
        self.result_label_text.setText(f"Morse to Text: {text}")

    def play_morse_sound(self):
        if self.morse_code:
            self.generate_morse_sound(self.morse_code)
        else:
            self.result_label_morse.setText("Please convert text to Morse first.")


    def generate_morse_sound(self, morse_code):
        sample_rate = 44100
        dot_duration = 0.1
        dash_duration = 0.2
        frequency = 500
        audio_data = []

        for symbol in morse_code:
            if symbol == '.':
                audio_data.extend(self.generate_tone(dot_duration, frequency, sample_rate))
            elif symbol == '-':
                audio_data.extend(self.generate_tone(dash_duration, frequency, sample_rate))
            else:
                audio_data.extend([0] * int(sample_rate * 0.2))

        # Convert audio data to a WAV format
        audio_data = np.array(audio_data)
        audio_data = (audio_data * 32767).astype(np.int16)

        # Save the audio to a temporary file
        file_name = "morse_code.wav"
        with wave.open(file_name, 'wb') as file:
            file.setnchannels(1)
            file.setsampwidth(2)
            file.setframerate(sample_rate)
            file.writeframes(audio_data.tobytes())

        # Play sound using pygame
        sound = pygame.mixer.Sound(file_name)
        sound.play()

    def generate_tone(self, duration, frequency, sample_rate):
        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
        return np.sin(2 * np.pi * frequency * t)