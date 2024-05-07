import pygame as pg
import pytmx
import os
# répertoire du script actuel
current_directory = os.path.dirname(os.path.abspath(__file__))

# répertoire de travail pour inclure le dossier parent
os.chdir(current_directory)
import pygame as pg
import pytmx
import os

class TiledMap:
    def __init__(self, filename):
        self.filename = filename
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    # Calculer les coordonnées isométriques
                    x_iso = (x - y) * (self.tmxdata.tilewidth / 2)
                    y_iso = (x + y) * (self.tmxdata.tileheight / 2)

                    # Ajouter un décalage pour centrer les tuiles
                    x_offset = (surface.get_width() / 2) + x_iso
                    y_offset = y_iso

                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x_offset, y_offset))

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface

if __name__ == "__main__":
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # Centrer la fenêtre au démarrage
    pg.init()
    pg.display.set_caption('Map isométrique')
    win = pg.display.set_mode((0, 0), pg.FULLSCREEN | pg.SRCALPHA) # Initialiser la fenêtre avant de charger la carte TMX
    iso = TiledMap("ressources/map/map_3.tmx")
    running = True
    zoom_factor = 1.0  # Facteur de zoom initial

    while running:
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                running = False
            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_UP:
                    zoom_factor += 0.1  # Augmenter le facteur de zoom
                elif ev.key == pg.K_DOWN:
                    zoom_factor -= 0.1  # Diminuer le facteur de zoom

        win.fill((0, 0, 0))  # Effacer l'écran avec une couleur de fond noire
        zoomed_map = pg.transform.scale(iso.make_map(), (int(iso.width * zoom_factor), int(iso.height * zoom_factor)))
        win.blit(zoomed_map, (0, 0))  # Afficher la carte redimensionnée
        pg.display.flip()

    pg.quit()
