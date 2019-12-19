import pygame as pg

from players.car_controlls import CarControl


class Keyboard:
    def get_move(self, sight_points=None, reward=None):
        keys = pg.key.get_pressed()
        moves = CarControl()
        moves.forward = True
        # if keys[pg.K_LEFT] or keys[pg.K_a]:
        #     moves.left = True
        # if keys[pg.K_RIGHT] or keys[pg.K_d]:
        #     moves.right = True
        # if keys[pg.K_UP] or keys[pg.K_w]:
        #     moves.forward = True
        # if keys[pg.K_DOWN] or keys[pg.K_s]:
        #     moves.backward = True
        return moves
