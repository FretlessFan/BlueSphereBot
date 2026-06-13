from enum import Enum

import numpy as np
import gymnasium as gym
from gymnasium import spaces
import bluesphere_visualizer
import os
import copy

from bluesphere_visualizer import full_score


class Action(Enum):
    ADV = 0
    LEFT = 1
    RIGHT = 2
    SNAP = 3
    JUMP_ONE = 4
    JUMP_TWO = 5

class BlueSphereEnv(gym.Env):

    def __init__(self,render_mode=None):

        self.observation_space = spaces.Dict(
            {
            "grid": spaces.Box(
            low=0,
            high=6,
            shape=(16, 16),
            dtype=np.int32
        ),
            "direction": spaces.Box(
                low=0,
                high=3,
                shape=(),
                dtype=np.int32
        ),

            "reverse": spaces.Box(
                low=0,
                high=1,
                shape=(),
                dtype=np.int32
        ),

            "stage_cleared": spaces.Box(
                low=0,
                high=1,
                shape=(),
                dtype=np.int32
        ),
            }
        )

        self.action_space = spaces.Discrete(6)

        assert render_mode is None
        self.render_mode = render_mode


    def convert_direction_to_num(self,direction):
        if direction == "N":
            return 0
        elif direction == "E":
            return 1
        elif direction == "S":
            return 2
        else:
            return 3

    def convert_reverse_to_num(self,reverse):
        return 1 if reverse else 0

    def reset(self,seed=None,options=None):
        super().reset(seed=seed)
        self.turn_count = 0
        self.stage_select = self.np_random.integers(0, 128, size=1, dtype=int)
        blue_spheres_saves_location = ".//Blue_Spheres_Data//"
        blue_speres_files = os.listdir(blue_spheres_saves_location)
        self.raw_stage = np.load(blue_spheres_saves_location + blue_speres_files[self.stage_select])
        self.player = bluesphere_visualizer.Player(3,15)
        self.true_map = copy.copy(self.raw_stage)
        self.show_map = np.array(bluesphere_visualizer.make_show_map(self.true_map, self.player))

        observation = {
            "grid": self.show_map,
            "direction": self.convert_direction_to_num(self.player.get_direction()),
            "reverse": self.convert_reverse_to_num(self.player.get_reverse()),
            "stage_cleared": 0
            }

        info = "Loaded This Level,", blue_speres_files[self.stage_select]

        return observation, info

    def convert_action_to_text(self,action):
        if(action == 0):
            return "adv"
        elif(action == 1):
            return "left"
        elif(action == 2):
            return "right"
        elif(action == 3):
            return "snap"
        elif(action == 4):
            return "jump_one"
        elif(action == 5):
            return "jump_two"
        else:
            return "ERROR"

    def stage_completed(self,stage_state):
        return not (np.count_nonzero((stage_state == 1) | (stage_state == 5)) > 0)

    def step(self,action):
        self.turn_count = self.turn_count + 1
        terminated = False
        self.true_map, self.show_map, self.initial_row, self.initial_col, self.move, self.circuit_map, score = bluesphere_visualizer.evaluate_move(self.show_map, self.true_map,
                                                                                               self.convert_action_to_text(action), self.player)

        self.true_map, bonus_points = bluesphere_visualizer.convert_ensnare(bluesphere_visualizer.neo_ensnare(self.true_map), self.true_map, self.player)
        self.show_map = bluesphere_visualizer.make_show_map(self.true_map, self.player)
        full_score = score + bonus_points

        completed = self.stage_completed(self.true_map)

        if completed:
            distance = np.linalg.norm(np.array([self.player.get_Row(),self.player.get_Col()]) - np.array([15,3]))
            if distance == 0:
                full_score = 40
                terminated = True
            else:
                full_score = full_score - (distance / 5)


        if (self.player.is_dead()):
            full_score = -10
            terminated = True


        observation = {
            "grid": self.show_map,
            "direction": self.convert_direction_to_num(self.player.get_direction()),
            "reverse": self.convert_reverse_to_num(self.player.get_reverse()),
            "stage_cleared": 1 if completed else 0,
            }

        return observation, full_score, terminated, self.turn_count >= 200 ,("Points:",full_score)