import pygame

class Inventory:
    def __init__(self, screen):
        self.screen = screen
        self.items = []  # List to store items
        self.slots = []  # List to store slot positions
        self.slot_size = 50  # Size of each slot (width and height)
        self.dragging_item = None
        self.rect = pygame.Rect(300, 100, 600, 600)  # Inventory window size and position
        self.setup_slots(10, 50, 8, 6)  # Setup inventory slots inside the window
        self.offset_x = 0
        self.offset_y = 0
        self.dragging = False  # To move the inventory window

    def draw(self):
        # Draw inventory window
        pygame.draw.rect(self.screen, (50, 50, 50), self.rect)
        # Draw inventory slots
        for slot in self.slots:
            pygame.draw.rect(self.screen, (255, 255, 255), slot, 2)
        # Draw items in inventory
        for item in self.items:
            self.screen.blit(item['image'], item['rect'])

    def add_item(self, item):
        self.items.append(item)

    def setup_slots(self, x, y, rows, cols):
        self.slots = []  # Clear existing slots
        for row in range(rows):
            for col in range(cols):
                slot_rect = pygame.Rect(self.rect.x + x + col * self.slot_size,
                                        self.rect.y + y + row * self.slot_size,
                                        self.slot_size, self.slot_size)
                self.slots.append(slot_rect)

    def populate_inventory(self, player_inventory):
        self.items.clear()
        for category, items in player_inventory.items():
            for item in items:
                self.add_item(self.create_item(item))

    def create_item(self, item_data):
        try:
            image = pygame.image.load(item_data['image']).convert_alpha()
        except pygame.error as e:
            print(f"Cannot load image: {item_data['image']}, {e}")
            image = pygame.Surface((self.slot_size, self.slot_size))
            image.fill((255, 0, 0))  # Red square if image not found
        rect = image.get_rect()
        rect.topleft = self.find_empty_slot()
        return {'name': item_data['name'], 'image': image, 'rect': rect, 'stats': item_data['stats']}

    def find_empty_slot(self):
        for slot in self.slots:
            if not any(item['rect'].colliderect(slot) for item in self.items):
                return slot.topleft
        return (0, 0)  # If no empty slot found

    def start_drag(self, pos):
        for item in self.items:
            if item['rect'].collidepoint(pos):
                self.dragging_item = item
                break

    def stop_drag(self, pos, player):
        if self.dragging_item:
            for slot in self.slots:
                if slot.collidepoint(pos):
                    self.dragging_item['rect'].topleft = slot.topleft
                    player.equip_item(self.dragging_item)
                    break
            self.dragging_item = None

    def drag(self, pos):
        if self.dragging_item:
            self.dragging_item['rect'].center = pos

    def handle_events(self, event, player):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if self.rect.collidepoint(event.pos):
                    self.offset_x = event.pos[0] - self.rect.x
                    self.offset_y = event.pos[1] - self.rect.y
                    self.dragging = True
                self.start_drag(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left click
                self.stop_drag(event.pos, player)
                self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.rect.x = event.pos[0] - self.offset_x
                self.rect.y = event.pos[1] - self.offset_y
                self.update_slots()

    def update_slots(self):
        slot_idx = 0
        for row in range(8):
            for col in range(6):
                self.slots[slot_idx].x = self.rect.x + 10 + col * self.slot_size
                self.slots[slot_idx].y = self.rect.y + 50 + row * self.slot_size
                slot_idx += 1

        for item in self.items:
            slot = self.slots[self.items.index(item)]
            item['rect'].topleft = slot.topleft