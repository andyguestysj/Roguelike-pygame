import os

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GREY = (40, 40, 40)
LIGHT_GREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)

# Screen
SCREEN_TITLE = "Roguelike"
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FRAMERATE = 30
BACKGROUND_COLOUR = BLACK

# Grid
IMAGE_SIZE = 4
SPRITE_SIZE = 32
COLOUR_KEY = MAGENTA
GRID_WIDTH = SCREEN_WIDTH / SPRITE_SIZE
GRID_HEIGHT = SCREEN_HEIGHT / SPRITE_SIZE

# Input
KEYBOARD_REPEAT_THRESHOLD = 1  # ms
KEYBOARD_REPEAT_INTERVAL = 150 # ms

# Resources
RESOURCES_FOLDER = os.path.join(".", "resources")
HIGHSCORE = os.path.join(RESOURCES_FOLDER, "highscore.txt")
WINDOW_ICON = os.path.join(RESOURCES_FOLDER, "icon.png")
SPRITE_SHEET = os.path.join(RESOURCES_FOLDER, "sprites.png")
FONT_FILE = os.path.join(RESOURCES_FOLDER, "font.ttf")

HIT_SOUND = [os.path.join(RESOURCES_FOLDER, f"hit_{x}.wav") for x in range(4)]
PLAYER_PICKUP_COIN_SOUND = os.path.join(RESOURCES_FOLDER, "coin_pickup.wav")
PLAYER_PICKUP_KEY_SOUND = os.path.join(RESOURCES_FOLDER, "key_pickup.wav")

# Animations and sprites
ANIMATION_INTERVAL = 500
PLAYER_ANIMATION_FRAMES = [
    [(0, 5), (1, 5)],
    [(2, 5), (3, 5)],
    [(4, 5), (5, 5)],
    [(6, 5), (7, 5)]
]
ENEMY_ANIMATION_FRAMES = [
    [(0, 4), (1, 4)],
    [(2, 4), (3, 4)],
    [(4, 4), (5, 4)],
    [(6, 4), (7, 4)]
]
PICKUP_ANIMATION_FRAMES = [
    [(4, 6), (5, 6)],
    [(5, 3)]
]
SHADOW_FRAMES = [
    (6, 6)
]
FLOOR_FRAMES = [
    (1, 3), (2, 3), (3, 3), (1, 1), (5,  1)
]
WALL_FRAMES = [
    [(1, 0), (1, 2), (1, 0), (0, 2), (0, 1), (0, 1), (0, 0), (0, 1), (1, 2), (2, 2), (1, 0), (1, 0), (2, 0), (0, 1), (0, 1), (0, 1)],
    [(4, 3)]
]

UI_HEALTH = [
    (0, 6), (1, 6), (2, 6), (3, 6)
]
UI_KEY = (5, 3)
UI_COIN = (4, 6)

# Entity stats
# [damage, health, hit_resistance, accuracy]
ENEMY_STATS = [
    [  1, 3,  0.1,  0.3],
    [0.25, 4, 0.15, 0.6],
    [  3, 2, 0.05,  0.5],
    [1.5, 8, 0.35, 0.35]
]

PLAYER_STATS = [
    1, 15, 0.25, 0.5
]

BASE_HIT_CHANCE = 0.1

# Points
STAGE_POINTS = 10
COIN_POINTS = 25
ENEMY_KILL_POINTS = 50