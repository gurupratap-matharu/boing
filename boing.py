import sys
from enum import Enum

import pgzero
import pgzrun
import pygame

if sys.version_info < (3, 5):
    print(
        "This game requires at least version 3. 5 of Python. Please download"
        "it from www.python.org"
    )
    sys.exit()

pgzero_version = [int(s) for s in pgzero.__version__.split(".")]
if pgzero_version < [1, 2]:
    print(
        "This game requires at least version 1.2 of PyGame Zero. You are"
        "using version {pgzero.__version__}. Please upgrade using the command"
        "'pip install --upgrade pgzero'"
    )
    sys.exit()

WIDTH = 800
HEIGHT = 480
TITLE = "Boing!"

HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
PLAYER_SPEED = 6
MAX_AI_SPEED = 6

NUM_PLAYERS = 1
SPACE_DOWN = False


class Ball(Actor):
    def __init__(self, dx):
        super().__init__("ball", (0, 0))
        self.x, self.y = HALF_WIDTH, HALF_HEIGHT
        self.dx, self.dy = dx, 0
        self.speed = 5

    def update(self):
        pass


class Bat(Actor):
    def __init__(self, player, move_func=None):
        x = 40 if player == 0 else 760
        y = HALF_HEIGHT
        super().__init__("blank", (x, y))

        self.player = player
        self.score = 0
        self.timer = 0
        self.move_func = move_func or self.ai

    def update(self):
        pass

    def ai(self):
        pass


class Game:
    def update(self):
        pass

    def draw(self):
        print("veer drawing game...")

    def play_sound(self):
        pass


def update():
    print("Veer updating...")


def draw():
    game.draw()


class State(Enum):
    MENU = 1
    PLAY = 2
    GAME_OVER = 3


# Try to play the theme music when the game starts. Incase an error occurs
# like no sound device just ignore it.
try:
    pygame.mixer.quit()
    pygame.mixer.init(44100, -16, 2, 1024)

    music.play("theme")
    music.set_volume(0.3)

except Exception:
    pass

# Set the initial game state
state = State.MENU

# Initially create a new game without any players
game = Game()

# Tell pygame zero to start - this line is needed sometimes
# when running the game from an IDE
pgzrun.go()
