'''
This calculates a 'vector' towards the player and randomly updates it based
on the player's location. This is a bit more complex, but more interesting
way of following the player.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_collect_coins
'''


import random
import arcade
import math
import os

# --- Constants ---
SPRITE_SCALING_PLAYER = 2
MONSTER_SCALING_IMG = 2
MONSTER_COUNT = 10
MONSTER_SPEED = 1.5

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 550

SPRITE_SPEED = 3

class monster(arcade.Sprite):
    """
    This class represents the coins on our screen. It is a child class of
    the arcade library's "Sprite" class.
    """
    def follow_sprite(self, player_sprite):
        """
        This function will move the current sprite towards whatever
        other sprite is specified as a parameter.

        We use the 'min' function here to get the sprite to line up with
        the target sprite, and not jump around if the sprite is not off
        an exact multiple of SPRITE_SPEED.
        """

        self.center_x += self.change_x
        self.center_y += self.change_y

        # Random 1 in 100 chance that we'll change from our old direction and
        # then re-aim toward the player
        if random.randrange(100) == 0:
            start_x = self.center_x
            start_y = self.center_y

            # Get the destination location for the bullet
            dest_x = player_sprite.center_x
            dest_y = player_sprite.center_y

            # Do math to calculate how to get the bullet to the destination.
            # Calculation the angle in radians between the start points
            # and end points. This is the angle the bullet will travel.
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            # Taking into account the angle, calculate our change_x
            # and change_y. Velocity is how fast the bullet travels.
            self.change_x = math.cos(angle) * MONSTER_SPEED
            self.change_y = math.sin(angle) * MONSTER_SPEED

class MyGame(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Gear Heart")

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Variables that will hold sprite lists
        self.player_list = None
        self.monster_list = None
        use_spatial_hash = False
        # Set up the player info
        self.player_sprite = None
        self.score = 0

        # Don't show the mouse cursor
        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.BROWN_NOSE)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.monster_list = arcade.SpriteList()
        # Score
        self.score = 0
        # Set up the player
        # Character image
        self.player_sprite = arcade.Sprite("sprites\man.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)
        # Create the monsters
        for i in range(MONSTER_COUNT):
            # Create the monsters instance
            # monster image
            monsters = monster("sprites\enemy.png", MONSTER_SCALING_IMG)
            # Position the monster
            monsters.center_x = random.randrange(SCREEN_WIDTH)
            monsters.center_y = random.randrange(SCREEN_HEIGHT)
            #makes sure the monsters do not spawn on top of the player
            if monsters.center_x or monsters.center_y <= player_sprite.center_x and player_sprite.center_y:
                monsters.center_x += 50
                monsters.center_y += 50
            else:
                break
            # Add the monster to the lists
            self.monster_list.append(monsters)

    def on_draw(self):
        """ Draw everything """
        arcade.start_render()
        self.monster_list.draw()
        self.player_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """
        # Move the center of the player sprite to match the mouse x, y
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def update(self, delta_time):
        """ Movement and game logic """
        #this will reduce the lag created by monsters that do not need collision detection
        self.monster_list.use_spatial_hash = False
        for monster in self.monster_list:
            monster.follow_sprite(self.player_sprite)

        # Generate a list of all sprites that collided with the player.
        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.monster_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for monster in hit_list:
            monster.kill()
            self.score -= 1

        self.monster_list.update()
def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()