import random
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


class Impact(Actor):
    def __init__(self, pos):
        super().__init__("blank", pos)
        self.time = 0

    def update(self):
        """
        Updates the sprite for impact. There are 5 impact sprites in all. We update to a new sprite every 2 frames.

        The game class controls the impact timer and resets it once it reaches 10.
        """

        self.image = "impact" + str(self.time // 2)
        self.time += 1


class Ball(Actor):
    """
    A Ball object of the game.

    The position of a ball in the game is given by its (x, y) attributes wheres its direction is given by dx and dy.

    Vectors dx and dy represent a unit vector

    A Ball also has a speed attribute which tells how many pixels it moves in each frame.
    """

    def __init__(self, dx):
        super().__init__("ball", (0, 0))
        self.x, self.y = HALF_WIDTH, HALF_HEIGHT
        self.dx, self.dy = dx, 0
        self.speed = 5

    def update(self):
        pass

    def is_out(self):
        """
        Checks if the ball has gone off the left or right edge of the screen.
        """

        return self.x < 0 or self.x > WIDTH


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
        """
        Updates the bat position at each frame i.e. 60 times per second.
        The main logic here is calculating the y-position with some sensible
        bounded limits.

        We also try to change the bat sprits based on the timer. The timer is updated externally when the ball is either lost or a new one is generated.
        """

        self.timer -= 1

        # First calculate the bat's y position either by player or ai
        y_movement = self.move_func()

        # Second apply it ensuring that the bat doesn't go through the
        # vertical walls
        self.y = min(400, max(80, self.y + y_movement))

        # Change the bat's sprite based on timer
        frame = 0

        if self.timer > 0:
            frame = 2 if game.ball.out() else 1

        self.image = "bat" + str(self.player) + str(frame)

    def ai(self):
        """
        Returns the no. of pixels to move in the y-direction based on the ball position
        """

        # check how far are we from the ball
        x_distance = abs(game.ball.x - self.x)

        # first target the vertical center of the screen
        target_y_1 = HALF_HEIGHT

        # second target the balls y-position with some margin of error
        target_y_2 = game.ball.y + game.ai_offset

        # calculate the weights based on how far is the ball
        weight_1 = min(1, x_distance / HALF_WIDTH)
        weight_2 = 1 - weight_1

        # calculate the resulting target
        target_y = (weight_1 * target_y_1) + (weight_2 * target_y_2)

        # cap movement to min/max limits to behave realistically
        target_y = min(MAX_AI_SPEED, max(-MAX_AI_SPEED, target_y - self.y))

        return target_y


class Game:
    """
    Represents the entire game of boing. It encompasses the two bats
    and a ball and is responsible for their life cycle.

    Note :

        Game is not an `Actor` but a generic object which controls all the actors i.e. bat, ball, impact.

    This is a common design pattern. Anything to do with our game like
        - is the game over?
        - has anyone won?
        - what's the score?
        - how to draw the game on screen?
        - how to update the bat, ball positions?

    are all dealt in this class.

    Hope you get the point.
    """

    def __init__(self, controls=(None, None)):
        """
        Instantiates a new game.

        The controls represent the callback function which change the
        movement of bats.
        If a control is None it represent a cpu player
        """

        self.bats = [Bat(0, controls[0]), Bat(0, controls[1])]
        self.ball = Ball(-1)

        # Short animations that are played when a ball bounces
        self.impacts = []

        # offset for the cpu player so it won't be able to hit the ball exactly in the center of the bat
        self.ai_offset = 0

    def update(self):
        """
        Updates all the active objects in the game.
        """

        all_game_objects = self.bats + [self.ball] + self.impacts

        for obj in all_game_objects:
            obj.update()

        # Remove expired impacts from the list
        self.impacts = [x for x in self.impacts if x.time < 10]

        # Update scores if the ball has gone off the left or right edge of the screen.

        if self.ball.out():
            scoring_player = 1 if self.ball.x < HALF_WIDTH else 0
            losing_player = 1 - scoring_player

            if self.bats[losing_player].timer < 0:
                self.bats[losing_player].score += 1

                game.play_sound("score_goal", 1)

                self.bats[losing_player].timer = 20

            elif self.bats[losing_player].timer == 0:
                direction = -1 if losing_player == 0 else 1
                self.ball = Ball(direction)

    def draw(self):
        """
        Paints a game on the screen
        """

        # Draw the fix table background
        screen.blit("table", (0, 0))

        # Show effect incase a point is "just scored"
        for player in (0, 1):
            if self.bats[player].timer > 0 and game.ball.is_out():
                screen.blit("effect" + str(player), (0, 0))

        # draw the bats, ball and impact effects in that order

        all_game_objects = self.bats + [self.ball] + self.impacts
        for obj in all_game_objects:
            obj.draw()

        # Displays the scores for each player
        for player in (0, 1):

            score = "{0:02d}".format(self.bats[player].score)

            for i in (0, 1):

                # get sprite for each score digit
                score_image = "digit0" + str(score[i])
                x = 255 + (160 * player) + (i * 55)
                y = 46

                screen.blit(score_image, (x, y))

    def play_sound(self, name, count=1, menu_sound=False):
        """
        Plays behavious based sound during the game.

        Some sounds have multiple varieties and we want to chose a random
        sound at any point of time, for this we pass count = n where a random int from 0 to n is suffixed to the original sound file

        """

        try:
            name += str(random.randint(0, count - 1))
            sound = getattr(sounds, name)
            print(f"sound: {sound}")
            sound.play()

        except Exception as e:
            pass


class State(Enum):
    """
    Defines the state of the game. Our game can only have three states perse

    Menu -> This is when the game starts and we are selecting players
    Play -> This is when we are actually playing the game
    Game Over -> Clearly the state when the game is over.
    """

    MENU = 1
    PLAY = 2
    GAME_OVER = 3


def update():
    """
    Pygame Zero runs this method 60 times per second automatically to 'update' the game. This develops the game 'flow'.

    We need not call this method manually as it's automatically done for us

    The logic for update will depend on what 'state' the game is into.
    In our boing context we are mostly updating
        - the players' scores
        - the state of game
        - checking if anyone won?
    """

    global NUM_PLAYERS, SPACE_DOWN, state, game

    # Check whether space key has just been pressed ans wasn't pressed in the previous frame
    space_pressed = False

    if keyboard.space and not SPACE_DOWN:
        space_pressed = True

    SPACE_DOWN = keyboard.space

    if state == State.MENU:

        if NUM_PLAYERS == 1 and keyboard.down:
            game.play_sound("down", menu_sound=True)
            NUM_PLAYERS = 2

        elif NUM_PLAYERS == 2 and keyboard.up:
            game.play_sound("up", menu_sound=True)
            NUM_PLAYERS = 1

    elif state == State.PLAY:
        if game.has_anyone_won():
            state = State.GAME_OVER
        else:
            game.update()

    elif state == State.GAME_OVER:
        if space_pressed:
            # Players wish to play again so start a new game
            state = State.MENU
            NUM_PLAYERS = 1

            # Create a new game object without any players
            game = Game()


def draw():
    """
    Pygame Zero runs this method 60 times per second to 'redraw' the game
    image on the screen. Just like screen painting.

    We need not call this method manually as it's already done for us.

    The logic for draw will depend on what 'state' of the game we are in
    and we basically call the `game.draw()` method as the game object
    itself knows how to draw itself on screen.
    """
    # TODO: put this game.draw() in a conditional state == State.PLAY
    game.draw()

    if state == State.MENU:
        menu_image = "menu" + str(NUM_PLAYERS - 1)
        screen.blit(menu_image, (0, 0))

    elif state == State.GAME_OVER:
        screen.blit("over", (0, 0))


# Try to play the theme music when the game starts. Incase an error occurs
# like no sound device just ignore it.
try:
    pygame.mixer.quit()
    pygame.mixer.init(44100, -16, 2, 1024)

    # music.play("theme")
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
