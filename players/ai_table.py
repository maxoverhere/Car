import json
import random
from os import path

import settings
from players.car_controlls import CarControl


class QLearning:
    def __init__(self):
        settings.AI_DATA_FILE = "q_learning_data"
        self.last_move = [0]
        self.last_position = [0]
        self.q_table: dict = {"[0][0]": -1}
        if path.exists(path.join(path.dirname(__file__), "..", "ai_data", settings.AI_DATA_FILE)):
            print("found existing ai data")
            with open(path.join(path.dirname(__file__), "..", "ai_data", "q_learning_data")) as infile:
                self.q_table: dict = json.load(infile)
            print(self.q_table.__len__())

    def save_data(self):
        with open(path.join(path.dirname(__file__), "..", "ai_data", "q_learning_data"), "w") as outfile:
            json.dump(self.q_table, outfile)

    def get_top_next_move_value(self, position: list):
        top_move_value = 0
        top_move = [random.randint(0, 1), random.randint(-1, 1)]
        position_hash = "["
        for i in position:
            position_hash += str(i)
        position_hash += "]["
        for i in range(0, 2):
            for j in range(-1, 2):
                cur_move_hash = position_hash + str(i) + str(j) + "]"
                if self.get_key_value(cur_move_hash) > top_move_value:
                    top_move_value = self.get_key_value(cur_move_hash)
                    top_move = [i, j]
        if random.randint(0, 3) == 0:
            return [random.randint(0, 1), random.randint(-1, 1)], top_move_value
        return top_move, top_move_value

    def get_move(self, sight_points, reward):
        next_move, best_move_value = self.get_top_next_move_value(sight_points)
        last_move_hash = compute_hash(self.last_position, self.last_move)
        last_move_value = self.get_key_value(last_move_hash)
        self.q_table[last_move_hash] = last_move_value + 0.8 * (reward + 0.8 * best_move_value - last_move_value)
        (self.last_position, self.last_move) = (sight_points, next_move)
        return CarControl(next_move)

    def get_key_value(self, key):
        if self.q_table.get(key) is None:
            return 0
        return self.q_table.get(key)

    def set_last_move_to_null(self):
        self.last_move = [0]
        self.last_position = [0]


def compute_hash(position: list, move: list):
    output = "["
    for i in position:
        output += str(i)
    output += "]["
    for i in move:
        output += str(i)
    return output + "]"
