from gym_examples.envs import bluesphere_visualizer
import os
import numpy as np
import copy
#from multiprocessing import Pool

from concurrent.futures import ProcessPoolExecutor

def convert_action_to_text(action):
    if (action == 0):
        return "adv"
    elif (action == 1):
        return "left"
    elif (action == 2):
        return "right"
    elif (action == 3):
        return "snap"
    elif (action == 4):
        return "jump_one"
    elif (action == 5):
        return "jump_two"
    else:
        return "ERROR"

def stage_completed(stage_state):
    return not (np.count_nonzero((stage_state == 1) | (stage_state == 5)) > 0)


def better_brutal_moves(true_map,player,move_list,show_map,max_moves=50):

    if(stage_completed(show_map)):
        return len(move_list),move_list,true_map

    if((len(move_list) > max_moves) or (player.is_dead())):
        return -1, [],true_map

    move_options = []
    for i in range(6):
        current_player = copy.deepcopy(player)
        true_map, show_map, initial_row, initial_col, move, circuit_map, score = bluesphere_visualizer.evaluate_move(show_map, true_map, convert_action_to_text(i), current_player)

        #print("true_map before convertensnare", true_map)
        print("Move:",move,"/:/",len(move_list))
        true_map, bonus_points = bluesphere_visualizer.convert_ensnare(
            bluesphere_visualizer.neo_ensnare(true_map,worth_it), true_map, current_player)
        show_map = np.array(bluesphere_visualizer.make_show_map(true_map, player),dtype=np.int32)
        full_score = score + bonus_points

        move_options.append(brutal_moves(true_map,current_player,move_list + [convert_action_to_text(i)],show_map,max_moves))

    true_moves = [elem for elem in move_options if elem[0] != -1]
    if(len(true_moves) == 0):
        return -1, [], true_map
    else:
        min_move = true_moves[0]

        for elem in true_moves:
            if elem[0] < min_move[0]:
                min_move = elem

        return min_move,true_moves,true_map



def brutal_moves(true_map,player,move_list,show_map,max_moves=50):

    if(stage_completed(show_map)):
        return len(move_list),move_list,true_map

    if((len(move_list) > max_moves) or (player.is_dead())):
        return -1, [],true_map

    move_options = []
    for i in range(6):
        current_player = copy.deepcopy(player)
        true_map, show_map, initial_row, initial_col, move, circuit_map, score = bluesphere_visualizer.evaluate_move(show_map, true_map, convert_action_to_text(i), current_player)

        #print("true_map before convertensnare", true_map)
        print("Move:",move,"/:/",len(move_list))
        true_map, bonus_points = bluesphere_visualizer.convert_ensnare(
            bluesphere_visualizer.neo_ensnare(true_map,worth_it), true_map, current_player)
        show_map = np.array(bluesphere_visualizer.make_show_map(true_map, player),dtype=np.int32)
        full_score = score + bonus_points

        move_options.append(brutal_moves(true_map,current_player,move_list + [convert_action_to_text(i)],show_map,max_moves))

    true_moves = [elem for elem in move_options if elem[0] != -1]
    if(len(true_moves) == 0):
        return -1, [], true_map
    else:
        min_move = true_moves[0]

        for elem in true_moves:
            if elem[0] < min_move[0]:
                min_move = elem

        return min_move,true_moves,true_map

blue_spheres_saves_location = "C://Users//wsreees//Downloads//moon//gym_examples//envs//Blue_Spheres_Data//"
spooky= os.listdir(blue_spheres_saves_location)
print(spooky)
len(spooky)
i = 0
print(spooky[i])
#donezo =np.load(blue_spheres_saves_location+)

raw_stage = np.load(blue_spheres_saves_location + spooky[i])
player = bluesphere_visualizer.Player(3, 15)
true_map = copy.deepcopy(raw_stage)
worth_it = bluesphere_visualizer.worth_processing(true_map)
np.place(true_map, true_map == 6, 0)
# print("true_map inception", true_map)
show_map = np.array(bluesphere_visualizer.make_show_map(true_map, player), dtype=np.int32)


big_brutes = brutal_moves(true_map,player,[],show_map,max_moves=30)


#
#
# # print("true_map post nuke", true_map)
# observation = {
#     "grid": show_map,
#     "direction": np.array([convert_direction_to_num(player.get_direction())], dtype=np.int32),
#     "reverse": np.array([convert_reverse_to_num(player.get_reverse())], dtype=np.int32),
#     "stage_cleared": np.array([0], dtype=np.int32),
#     "prev_move_turn": np.array([0], dtype=np.int32)
# }
# level_name = blue_spheres_files[int(stage_select[0])]
# info = {
#     "log": f"Loaded This Level, {level_name}"
# }
# print(info)
