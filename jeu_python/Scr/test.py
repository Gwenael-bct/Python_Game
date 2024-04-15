import random
from monstres.slime_test import Slime
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)

slimes = [Slime(random.randint(1, 5)) for _ in range(random.randint(1, 5))]

print(slimes)

print(*slimes)
