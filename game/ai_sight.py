from pygame.math import Vector2
from game.sprites import *
from game.tilemap import Map
from settings import *
from os import path
import copy
vec = Vector2
import math

class Sight:

    def __init__(self):
        map_folder = path.join(path.dirname(__file__), '..', 'maps')
        self.map = Map(path.join(map_folder, MAP_SELECTED))

    def check_tile(self, point):
        if point.x < 0 or point.y < 0 or point.x >= self.map.tilewidth or point.y >= self.map.tileheight:
            return False
        else:
            x = round(point.x) - 1
            y = round(point.y) - 1
            if self.map.data[y][x] == '1':
                return False
            return True

    def get_sight(self, pos: vec, player_angle):
        results = []
        start_point = (pos / TILESIZE)
        for angle in SIGHT_ANGLES:
            sight_point = copy.copy(start_point)
            sight_vec = vec(0.3, 0.0).rotate(angle - player_angle)
            num = 0
            while True:
                num += 1
                sight_point += sight_vec
                if not (self.check_tile(sight_point)):
                    break
            # results.append(round(math.log2(num)))
            results.append(round(math.log(num)))
        return results

    def get_sight_position(self, pos: vec, player_angle):
        results = []
        start_point = (pos / TILESIZE)
        for angle in SIGHT_ANGLES:
            sight_point = copy.copy(start_point)
            sight_vec = vec(0.3, 0.0).rotate(angle - player_angle)
            while True:
                sight_point += sight_vec
                if not (self.check_tile(sight_point)):
                    break
            sight_point = sight_point * TILESIZE
            results.append((round(sight_point.x), round(sight_point.y)))
        return results
