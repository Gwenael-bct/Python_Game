import random
import os

# répertoire du script actuel
current_directory = os.path.dirname(os.path.abspath(__file__))

# répertoire de travail pour inclure le dossier parent
os.chdir(current_directory)

class Item:
    items = {
        "bâton magique": {"name": "Bâton magique", "rarity": "S", "stats":{"magic_power": 15, "health": 30, "max_health": 30}, "price": 10, 
                        "description": "Bâton magique S permettant d'améliorer les dégâts magiques",
                        "image": "ressources/sprites/weapons/magic_bow.png"},
        # Ajoutez d'autres items ici
    }

    def __init__(self, name=None):
        if name is None:
            name = random.choice(list(self.items.keys()))
        item_details = self.items[name]
        self.name = name
        self.rarity = item_details["rarity"]
        self.magic_damage = item_details["stats"]["magic_power"]
        self.health = item_details["stats"]["health"]
        self.max_health = item_details["stats"]["max_health"]
        self.price = item_details["price"]
        self.description = item_details["description"]
        self.image = item_details["image"]

    @staticmethod
    def drop_random_item(name=None):
        """
        Choisis aléatoirement un item parmi ceux disponibles et le retourne.
        """
        if name is None:
            name = random.choice(list(Item.items.keys()))
        else:
            name = name
        return Item.items[name]
