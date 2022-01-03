from code.helper_functions.get_config import get_config

# Width And Height Of Display (Change in settings.toml - Not here!)
width, height = get_config()

# Width/Height/Sizes of Sprites
star_width = width // 120
star_height = star_width // 2
buggy_width = width // 15
laser_width_vertical = buggy_width // 12  # width of laser shot out of top of buggy
laser_height_vertical = laser_width_vertical * 2  # height of laser shot out of top of buggy
laser_width_horizontal = buggy_width // 3  # width of laser shot out of side of buggy
laser_height_horizontal = laser_width_horizontal // 8  # height of laser shot out of side of buggy
alien_laser_width = buggy_width // 12
alien_laser_height = alien_laser_width * 2
ammo_crate_width = width // 30
rock_width = width * 3 // 80
hole_width = width // 20
white_alien_width = width // 20
orange_alien_width = width // 20
purple_alien_width = width // 20
text_height = height // 12
ground_height = height // 12
hole_whitespace = 1/11  # collision box above hole ratio (change if texture is changed)

# Speeds of Sprites
white_alien_speed = white_alien_width // 15
orange_alien_speed = orange_alien_width // 15
purple_alien_speed = purple_alien_width // 20
alien_laser_speed = alien_laser_height // 2
laser_vertical_speed = laser_height_vertical // 2
laser_horizontal_speed = laser_width_horizontal // 2
star_speed = star_width // 10
mountain_speed = width // 200
buggy_centering_speed = buggy_width // 30  # speed with which buggy automatically returns to center
buggy_jump_height = (2.25/1080) * height
ground_speed = width * 3 // 400  # speeds of things on the ground (rocks, holes, etc.)

# Time Intervals (in milliseconds)
bonus_time = 30000  # continuous play time until bonus points awarded
update_animations_time = 100
initial_rock_spawn_time = 5000, 8000
initial_hole_spawn_time = 4000, 7000
initial_ammo_spawn_time = 25000, 30000

# Frequencies
white_alien_spawn_rate = 0.0015
orange_alien_spawn_rate = 0.002
purple_alien_spawn_rate = 0.0015
star_spawn_rate = 0.02
white_alien_shoot_rate = 0.005
orange_alien_shoot_rate = 0.01
purple_alien_shoot_rate = 0.02
rock_spawn_rate = 2000, 8000  # range in milliseconds
hole_spawn_rate = 2000, 8000
ammo_spawn_rate = 20000, 25000

# Amounts
lives = 3  # Starts with 3 lives
max_ammo = 50  # Starts out with and caps at 50 ammo
ammo_crate_amount = 25  # Every crate gives out 25 ammo
max_buggy_shoot_amount = 6  # Can have 6 bullets on screen
gravity = (0.05/1080) * height  # in game gravity
rock_jump_score = 80
rock_shoot_score = 100
hole_jump_score = 100
orange_alien_shoot_score = 100
purple_alien_shoot_score = 100
white_alien_shoot_score = 200
time_bonus_amount = 500
life_bonus_requirement = 10000  # How many points you need for an extra life


# Don't change!
def init():
    global points
    points = 0
