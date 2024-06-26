import pygame
import os

# répertoire du script actuel
current_directory = os.path.dirname(os.path.abspath(__file__))

# répertoire de travail pour inclure le dossier parent
os.chdir(current_directory)
class DialogBox:

    X_POSITION = 200
    Y_POSITION = 400

    def __init__(self):
        self.box = pygame.image.load('ressources/dialogs/dialog_box.png')
        self.box = pygame.transform.scale(self.box, (450, 50))
        self.texts = []
        self.text_index = 0
        self.letter_index = 0
        self.font = pygame.font.Font("ressources/dialogs/dialog_font.ttf", 12)
        self.reading = False

    def execute(self, dialog=[]):
        if self.reading:
            self.next_text()
        else:
            self.reading = True
            self.index = 0
            self.texts = dialog

    def render(self, screen):
        if self.reading:
            self.letter_index+=1

            if self.letter_index >= len(self.texts[self.text_index]):
                self.letter_index = self.letter_index

            screen.blit(self.box, (self.X_POSITION, self.Y_POSITION))
            text = self.font.render(self.texts[self.text_index][0:self.letter_index], False, (0, 0, 0))
            screen.blit(text, (self.X_POSITION + 25, self.Y_POSITION + 30))

    def next_text(self):
        self.text_index +=1
        self.letter_index = 0

        if self.text_index >=len(self.texts):
            self.text_index = 0
            self.letter_index = 0
            self.reading = False
