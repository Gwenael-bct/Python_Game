import os
import pygame

current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.position =[x, y]
        self.velocity = 5
        self.damage = 50
        self.images = self.load_animation_images()
        self.image = self.images[0]  # Initialiser avec la première image
        self.rect = self.image.get_rect(topleft=self.position)
        self.angle = 0
        self.current_image = 0  # Ajout de l'initialisation de current_image
        self.animation_counter = 0
        self.animation_delay = 5    

    def load_animation_images(self):
        images = []
        path = '../sort/fire_ball_'

        for num in range(1, 9):
            image_path = path + str(num) + '.png'
            img = pygame.image.load(image_path).convert()
            img.set_colorkey([0, 0, 0])
            img = pygame.transform.scale(img, (55, 35))
            images.append(img)

        return images

    def animate(self):
        # Met à jour l'image seulement toutes les N itérations
        if self.animation_counter % self.animation_delay == 0:
            self.current_image = (self.current_image + 1) % len(self.images)
            self.image = self.images[self.current_image]

    def rotate(self):
        # Tourner le projectile
        self.angle += 0
        rotated_image = pygame.transform.rotozoom(self.images[self.current_image], self.angle, 1)
        self.image = rotated_image.convert_alpha()  # Convertissez en mode alpha après la rotation
        self.rect = self.image.get_rect(center=self.rect.center)



    def move(self, direction):
        # Utilise la direction pour déplacer le projectile vers le monstre
        self.position[0] += self.velocity * direction[0]
        self.position[1] += self.velocity * direction[1]
        self.rect.topleft = self.position

#        self.rotate()