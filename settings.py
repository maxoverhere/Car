import pygame as pg
from players.ai_table import QLearning
from players.keyboard import Keyboard

RED = (255, 0, 0)
BROWN = (106, 55, 5)

# game settings
WIDTH = 1024  # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Tilemap Demo"
BGCOLOR = BROWN
MAP_SELECTED = 'map5.txt'

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

WALL_IMG = 'tileGreen_39.png'
REWARD_LINE_IMG = 'reward_line.png'

# Player settings
PLAYER_SPEED = 500
PLAYER_ROT_SPEED = 250
PLAYER_IMG = 'car.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)

# AI settings
PLAYER = QLearning()
# PLAYER = Keyboard()
SHOW_AI_SIGHT = True
SIGHT_ANGLES = (45, 8, -8, -45)
REWARD_LINES = [((200, 50), (200, 300)), ((300, 50), (300, 300)), ((500, 50), (500, 300)), ((700, 50), (700, 300)),
                ((1000, 50), (700, 300)), ((1000, 500), (800, 500))]
AI_DATA_FILE = "q_learning_data"
SKIP_VISUALS = False
LIMIT_FRAMES = True
LEARNING_MODE = True
DIE_WITHOUT_REWARD = True
