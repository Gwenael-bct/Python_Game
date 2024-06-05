import pygame
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)

class Inventaire:
    def __init__(self, screen):
        self.screen = screen
        self.width = 800
        self.height = 600
        self.rect = pygame.Rect(100, 100, self.width, self.height)
        self.color = (50, 50, 50)
        self.image = pygame.image.load("ressources/caracteristique/player.png")
        self.magic_bow = pygame.image.load("ressources/weapons/magic_bow.png")
        self.plus_image = pygame.transform.scale(self.image_plus, (20, 20))
        self.minus_image = pygame.transform.scale(self.image_minus, (25, 12))
        self.dragging = False
        self.plus_buttons = []
        self.minus_buttons = []
        self.selected_characteristic = None

    def render(self, player):
        if player.health < 0:
            player.health = 0
        if player.mana < 0:
            player.mana = 0
        pygame.draw.rect(self.screen, self.color, self.rect, border_radius=20)
        font_1 = pygame.font.Font(None, 18)
        font_2 = pygame.font.Font(None, 22)
        font = pygame.font.Font(None, 25)

        # Partie 1 : Image du joueur avec son niveau et les points
        section_y = self.rect.y + 10

        self.draw_section_border(section_y, 140, 10, 20)

        player_image = pygame.transform.scale(self.image, (80, 80))
        self.screen.blit(player_image, (self.rect.x + 20, section_y + 10))
        
        name_text = font.render("fsze", True, (255, 255, 255))
        level_text = font.render(f"Niveau: {player.level}", True, (255, 255, 255))
        points_text = font.render(f"{player.carac_points} points", True, (255, 255, 0))
        
        self.screen.blit(name_text, (self.rect.x + 110, section_y + 10))
        self.screen.blit(level_text, (self.rect.x + 110, section_y + 50))
        self.screen.blit(points_text, (self.rect.x + 110, section_y + 90))

        # Séparateur avec dégradé
        section_y += 150
        self.draw_gradient_separator(section_y)

        # Partie 2 : Barre d'expérience et d'énergie
        self.draw_section_border(section_y, 160, 10, 20)

        bar_height = 20
        bar_spacing = 50
        experience_text = font_1.render("Expérience:", True, (255, 255, 255))
        mana_text = font_1.render("Mana:", True, (255, 255, 255))
        vita_text = font_1.render("Vie:", True, (255, 255, 255))
        experience_text_2 = font_2.render(f"{player.xp} / {player.max_xp}", True, (0, 0, 0))
        mana_text_2 = font_2.render(f"{player.mana} / {player.max_mana}", True, (0, 0, 0))
        vita_text_2 = font_2.render(f"{player.health} / {player.max_health}", True, (0, 0, 0))

        pygame.draw.rect(self.screen, (255, 255, 255), (self.rect.x + 20, section_y + 30, 260, bar_height), border_radius=10)
        pygame.draw.rect(self.screen, (255, 0, 0), (self.rect.x + 20, section_y + 30, 260 * (player.xp/player.max_xp), bar_height), border_radius=10)
        self.screen.blit(experience_text, (self.rect.x + 20, section_y + 10))
        self.screen.blit(experience_text_2, (self.rect.x + 120, section_y + 35))

        pygame.draw.rect(self.screen, (255, 255, 255), (self.rect.x + 20, section_y + 30 + bar_spacing, 260, bar_height), border_radius=10)
        pygame.draw.rect(self.screen, (0, 0, 255), (self.rect.x + 20, section_y + 30 + bar_spacing, 260 *(player.mana/player.max_mana), bar_height), border_radius=10)
        self.screen.blit(mana_text, (self.rect.x + 20, section_y + 10 + bar_spacing))
        self.screen.blit(mana_text_2, (self.rect.x + 120, section_y + 35 + bar_spacing))

        pygame.draw.rect(self.screen, (255, 255, 255), (self.rect.x + 20, section_y + 30 + bar_spacing*2, 260, bar_height), border_radius=10)
        pygame.draw.rect(self.screen, (0, 255, 0), (self.rect.x + 20, section_y + 30 + bar_spacing*2, 260 * (player.health/player.max_health), bar_height), border_radius=10)
        self.screen.blit(vita_text, (self.rect.x + 20, section_y + 10 + bar_spacing*2))
        self.screen.blit(vita_text_2, (self.rect.x + 120, section_y + 35 + bar_spacing*2))

        # Séparateur avec dégradé
        section_y += 170
        self.draw_gradient_separator(section_y)

        # Partie 3 : Caractéristiques du joueur
        self.draw_section_border(section_y, 360, 10, 20)

        stats_y_start = section_y + 10
        line_spacing = 30  # Espacement entre les lignes
        vitality_text = font.render(f"Vitalité: {player.health}", True, (255, 255, 255))
        wisdom_text = font.render(f"Sagesse: {player.wisdom}", True, (255, 255, 255))
        magic_text = font.render(f"Force: {player.magic_power}", True, (255, 255, 255))
        strength_text = font.render(f"Force: {player.physic_power}", True, (255, 255, 255))
        luck_text = font.render(f"Chance: {player.luck}", True, (255, 255, 255))
        agility_text = font.render(f"Agilité: {player.dexterity}", True, (255, 255, 255))

        characteristics = [
            ('Vitalité', player.health),
            ('Sagesse', player.wisdom), 
            ('Force', player.physic_power),
            ('Magie', player.magic_power),
            ('Chance', player.luck), 
            ('Agilité', player.dexterity)
        ]

        self.plus_buttons = []  # Clear the previous plus buttons
        self.minus_buttons = []  # Clear the previous minus buttons

        for i, (label, value) in enumerate(characteristics):
            text = font.render(f"{label}: {value}", True, (255, 255, 255))
            points_text = font.render(f"{player.allocated_points[label]}", True, (255, 255, 0))
            self.screen.blit(text, (self.rect.x + 50, stats_y_start + i * line_spacing))
            self.screen.blit(points_text, (self.rect.x + 200, stats_y_start + i * line_spacing))
            if player.carac_points > 0:
                plus_rect = self.plus_image.get_rect(topleft=(self.rect.x + 260, stats_y_start + i * line_spacing))
                self.screen.blit(self.plus_image, plus_rect.topleft)
                self.plus_buttons.append((plus_rect, label))
            if player.allocated_points[label] > 0:
                minus_rect = self.minus_image.get_rect(topleft=(self.rect.x + 230, stats_y_start + i * line_spacing))
                self.screen.blit(self.minus_image, minus_rect.topleft)
                self.minus_buttons.append((minus_rect, label))
            if i < len(characteristics):
                pygame.draw.line(self.screen, (19, 75, 59), 
                                 (self.rect.x + 50, stats_y_start + (i + 1) * line_spacing - 5), 
                                 (self.rect.x + self.width - 50, stats_y_start + (i + 1) * line_spacing - 5), 1)
                
        # Partie 4 : Caractéristiques du joueur à répartir
        section_y += line_spacing*7
        self.draw_section_border(section_y, 30, 50, 100, 0)
        points_text = font.render(f"Points à répartir: {player.carac_points}", True, (255, 255, 0))
        self.screen.blit(points_text, (self.rect.x + 60, section_y + 5))

    def draw_section_border(self, y, height, x, width, border_radius=10):
        section_rect = pygame.Rect(self.rect.x + x, y, self.width - width, height)
        pygame.draw.rect(self.screen, (19, 75, 59), section_rect, 2, border_radius)

    def draw_gradient_separator(self, y):
        half_width = self.width // 2 - 10  # Subtracting padding
        for i in range(self.rect.width - 20):
            distance_to_center = abs(i - half_width)
            color_value1 = 50 + (19 * (1 - distance_to_center / half_width))
            color_value2 = 50 + (75 * (1 - distance_to_center / half_width))
            color_value3 = 50 + (59 * (1 - distance_to_center / half_width))
            color_value1 = int(color_value1)
            color_value2 = int(color_value2)
            color_value3 = int(color_value3)
            pygame.draw.line(self.screen, (color_value1, color_value2, color_value3), 
                            (self.rect.x + 10 + i, y - 5), 
                            (self.rect.x + 10 + i, y - 7))
            
    def handle_events(self, event, player):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Vérifier si le clic est dans la fenêtre d'inventaire
                if self.rect.collidepoint(mouse_x, mouse_y):
                    # Enregistrer l'offset par rapport à la position de la souris
                    self.offset_x = mouse_x - self.rect.x
                    self.offset_y = mouse_y - self.rect.y
                    self.dragging = True  # Initialiser la variable dragging
                
                # Vérifier si un bouton plus ou moins est cliqué
                for plus_rect, label in self.plus_buttons:
                    if plus_rect.collidepoint(mouse_x, mouse_y):
                        self.selected_characteristic = ('plus', label)
                for minus_rect, label in self.minus_buttons:
                    if minus_rect.collidepoint(mouse_x, mouse_y):
                        self.selected_characteristic = ('minus', label)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Relâchement du clic gauche
                self.dragging = False
                if self.selected_characteristic:
                    action, label = self.selected_characteristic
                    if action == 'plus' and player.carac_points > 0:
                        if label == 'Vitalité':
                            player.health += 10
                            player.max_health += 10
                        elif label == 'Sagesse':
                            player.wisdom += 1
                        elif label == 'Magie':
                            player.magic_power += 1
                        elif label == 'Force':
                            player.physic_power += 1
                        elif label == 'Chance':
                            player.luck += 1
                        elif label == 'Agilité':
                            player.dexterity += 1
                        player.allocated_points[label] += 1
                        player.carac_points -= 1
                    elif action == 'minus' and player.allocated_points[label] > 0:
                        if label == 'Vitalité':
                            player.health -= 10
                            player.max_health -= 10
                        elif label == 'Sagesse':
                            player.wisdom -= 1
                        elif label == 'Magie':
                            player.magic_power -= 1
                        elif label == 'Force':
                            player.physic_power -= 1
                        elif label == 'Chance':
                            player.luck -= 1
                        elif label == 'Agilité':
                            player.dexterity -= 1
                        player.allocated_points[label] -= 1
                        player.carac_points += 1
                    self.selected_characteristic = None

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                # Déplacer la fenêtre d'inventaire en fonction du mouvement de la souris
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.rect.x = mouse_x - self.offset_x
                self.rect.y = mouse_y - self.offset_y
