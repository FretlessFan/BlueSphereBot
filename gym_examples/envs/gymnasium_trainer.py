from enum import Enum

import numpy as np
import gymnasium as gym
from gymnasium import spaces
from gym_examples.envs import bluesphere_visualizer
from generate_stages import Blue_Generator
import os
import copy


#DEFINING COLORS
BLUE = 1
RED = 2
BUMPER = 3
SPRING = 4
RING = 5

class Action(Enum):
    ADV = 0
    LEFT = 1
    RIGHT = 2
    SNAP = 3
    JUMP_ONE = 4
    JUMP_TWO = 5

class BlueSphereEnv(gym.Env):

    def __init__(self,render_mode=None):

        self.show_map = None
        self.worth_it = None
        self.true_map = None
        self.player = None
        self.turn_count = None
        self.stage_select = None
        self.raw_stage = None
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
                shape=(1,),
                dtype=np.int32
        ),

            "reverse": spaces.Box(
                low=0,
                high=1,
                shape=(1,),
                dtype=np.int32
        ),

            "stage_cleared": spaces.Box(
                low=0,
                high=1,
                shape=(1,),
                dtype=np.int32
        ),
            "prev_move_turn": spaces.Box(
                low=0,
                high=1,
                shape=(1,),
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

    def find_player(self,grid):
        row,col = -1,-1
        for i in range(16):
            for j in range(16):
                if(grid[i][j] == 6):
                    return i,j

        return row,col

    def level_grabber(self,generate=True,chunks=None):
        if(generate):
            selected_value = self.np_random.integers(0, len(chunks), size=1, dtype=int)[0]
            selected_chunk = chunks[selected_value]
            blue_sphere_gen = Blue_Generator(chunks=selected_chunk["chunk"],stage_names=selected_chunk["name"])
            raw_stage = blue_sphere_gen.generate()
            self.stage_select = ("Random Generated",selected_chunk["name"])
            return raw_stage
        else:
            blue_spheres_saves_location = "C://Users//bretstev//Downloads//moon//gym_examples//envs//Blue_Spheres_Data//"
            blue_spheres_files = os.listdir(blue_spheres_saves_location)
            self.stage_select = self.np_random.integers(0, len(blue_spheres_files), size=1, dtype=int)
            # self.raw_stage = np.load(blue_spheres_saves_location + blue_spheres_files[int(self.stage_select[0])])
            raw_stage = np.load(blue_spheres_saves_location + blue_spheres_files[int(0)])
            return raw_stage

    def reset(self,seed=None,options=None):
        super().reset(seed=seed)
        self.turn_count = 0


        current_chunks =[#{"name":"2by2","chunk":[{"num": 5, "chunk": [[RING]]}, {"num": 5, "chunk": [[BLUE, BLUE],
                         #                                                     [BLUE, BLUE]]}]},
                         # {"name": "super_simple", "chunk": [{"num": 3, "chunk": [[RING]]}, {"num": 2, "chunk": [[BLUE]],
                         #                                                                                }]},

                         {"name": "3by3", "chunk": [{"num": 2, "chunk": [[RING]]}, {"num": 4, "chunk": [[BLUE, BLUE,BLUE],
                                                                                                        [BLUE, BLUE,BLUE],
                                                                                                        [BLUE,BLUE,BLUE]]}]},
                         {"name": "bad_bumpers",
                          "chunk": [{"num": 7, "chunk": [[RING]]}, {"num": 3, "chunk": [[0, 0, 0],
                                                                                        [0, BUMPER, 0],
                                                                                        [0, 0, 0]]}]},

                         ]

        self.raw_stage = self.level_grabber(generate=False,chunks=current_chunks)
        row,col= self.find_player(self.raw_stage)
        self.player = bluesphere_visualizer.Player(row, col)
        self.true_map = copy.deepcopy(self.raw_stage)
        self.worth_it = bluesphere_visualizer.worth_processing(self.true_map)
        np.place(self.true_map, self.true_map == 6, 0)
        #print("self.true_map inception", self.true_map)
        self.show_map = np.array(bluesphere_visualizer.make_show_map(self.true_map, self.player),dtype=np.int32)
        #print("self.true_map post nuke", self.true_map)
        observation = {
            "grid": self.show_map,
            "direction": np.array([self.convert_direction_to_num(self.player.get_direction())],dtype=np.int32),
            "reverse": np.array([self.convert_reverse_to_num(self.player.get_reverse())],dtype=np.int32),
            "stage_cleared": np.array([0], dtype=np.int32),
            "prev_move_turn": np.array([0], dtype=np.int32)
        }
        #level_name = blue_spheres_files[int(self.stage_select[0])]
        # level_name = blue_spheres_files[int(0)]

        info = {
            "log": f"Loaded This Level, random"
        }
        print(info)
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
        action_text = self.convert_action_to_text(action)
        is_turning = action_text in ["left", "right"]

        # Check if this is an illegal double-turn
        if is_turning and self.player.get_prev_move_turn():
            # RETURN EARLY: No move made, small penalty, episode continues
            reward = -1.0
            self.turn_count += 1
            completed = self.stage_completed(self.true_map)
            prev_move = self.player.get_prev_move_turn()
            # Construct same observation as before
            observation = self.get_observation(completed,prev_move)
            return observation, float(reward), False, self.turn_count >= 400, {"log": "Illegal turn"}



        # Check if this is an illegal double-turn
        if (action_text == "snap") and (self.player.get_reverse() == False):
            # RETURN EARLY: No move made, small penalty, episode continues
            reward = -1.0
            self.turn_count += 1
            completed = self.stage_completed(self.true_map)
            prev_move = self.player.get_prev_move_turn()
            # Construct same observation as before
            observation = self.get_observation(completed, prev_move)
            return observation, float(reward), False, self.turn_count >= 200, {"log": "Illegal snap"}

        self.turn_count = self.turn_count + 1
        terminated = False
        #print("self.true_map before itallll", self.true_map)
        self.true_map, self.show_map, self.initial_row, self.initial_col, self.move, self.circuit_map, score = bluesphere_visualizer.evaluate_move(self.show_map, self.true_map,
                                                                                                                                                self.convert_action_to_text(action), self.player)

        #print("self.true_map before convertensnare", self.true_map)
        #print("Move:",self.move)
        self.true_map, bonus_points = bluesphere_visualizer.convert_ensnare(
            bluesphere_visualizer.neo_ensnare(self.true_map,self.worth_it), self.true_map, self.player)
        self.show_map = np.array(bluesphere_visualizer.make_show_map(self.true_map, self.player),dtype=np.int32)
        full_score = score + bonus_points

        completed = self.stage_completed(self.true_map)
        prev_move = self.player.get_prev_move_turn()

        if completed:
            distance = np.linalg.norm(np.array([self.player.get_Row(),self.player.get_Col()]) - np.array([15,3]))
            if distance == 0:
                full_score += 100.0  # Massive payout for ultimate victory condition
                terminated = True
            else:
                # Small penalty for every tile away from the exit when cleared
                full_score -= float(distance * 0.5)


        if (self.player.is_dead()):
            full_score = -10
            terminated = True

        observation = self.get_observation(completed,prev_move)

        return observation, full_score, terminated, self.turn_count >= 200 , {"points": full_score}

    def get_observation(self,completed,prev_move):
        return {
            "grid": self.show_map,
            "direction": np.array([self.convert_direction_to_num(self.player.get_direction())],dtype=np.int32),
            "reverse": np.array([self.convert_reverse_to_num(self.player.get_reverse())],dtype=np.int32),
            "stage_cleared": np.array([1 if completed else 0], dtype=np.int32),
            "prev_move_turn": np.array([1 if prev_move else 0], dtype=np.int32)
        }