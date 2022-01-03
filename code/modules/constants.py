from code.helper_functions.get_config import get_config

# General
width, height = get_config()

# Width/Height/Sizes of Sprites
star_width = None
star_height = None
laser_width_vertical = None
laser_height_vertical = None
laser_width_horizontal = None
laser_height_horizontal = None
alien_laser_width = None
alien_laser_height = None
ammo_crate_width = None
rock_width = None
hole_width = None
white_alien_width = None
orange_alien_width = None
purple_alien_width = None
buggy_width = None
text_height = None
hole_whitespace = 1/11

# Speeds of Sprites
white_alien_speed = None
orange_alien_speed = None
purple_alien_speed = None
alien_laser_speed = None
laser_speed = None
star_speed = None
mountain_speed = None
buggy_centering_speed = None
buggy_jump_height = None
ground_speed = width*3/400

# Time Intervals
bonus_time = None
update_animations_time = None

# Frequencies
white_alien_spawn_rate = None
orange_alien_spawn_rate = None
purple_alien_spawn_rate = None
rock_spawn_rate = None
hole_spawn_rate = None
star_spawn_rate = None
ammo_spawn_rate = None
white_alien_shoot_rate = None
orange_alien_shoot_rate = None
purple_alien_shoot_rate = None

# Amounts
lives = 3  # Starts with 3 lives
max_ammo = 50  # Starts out with and caps at 50 ammo
ammo_crate_amount = 25  # Every crate gives out 25 ammo
max_buggy_shoot_amount = 6  # Can have 6 bullets on screen

def init():
    global points
    points = 0
