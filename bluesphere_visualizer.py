import cv2

import numpy as np
import os
import copy

#DEFINING COLORS
BLUE = 1
RED = 2
BUMPER = 3
SPRING = 4
RING = 5

BASELINE = 7
MIN_NODE = BASELINE
NODE_ARRAY = []

#true_map = donezoj

"""
[[6, 10], [4, 10], [5, 9]]

"""

def get_corner_blue(location,true_map):
    print("hello")
    slider_corner = make_slider_corner()
    #print(len(slider_corner))
    #location = corner_list[]
    count = 0
    for elem in slider_corner:

        if(check_corner_type(location,RED,true_map,elem)):
            adder = np.array(elem[0])
            np.place(adder, adder == 0,1)
            done = np.array(location) + np.array(adder)
            print("HOOOO",done)
            return done

#
def find_all_corners(true_map):
    print("how")
    corner_list = []
    for i in range(len(true_map)):
        for j in range(len(true_map[i])):
            if(true_map[i][j]==RED):
                corna= is_corner([i,j],RED,true_map)
                if(corna):
                    corner_list.append([i,j])

    return corner_list

def neo_ensnare(true_map):
    corner_list = find_all_corners(true_map)
    if(0):
        elem = corner_list[0]

    crack_list = []
    for elem in corner_list:
#        if not elem in crack_list:
        path = find_shortest_path(elem, elem, [], true_map, RED, [])

        print("I am path",path)
        if(path[0] != -1):
            fill_list = get_fill(get_corner_blue(elem, true_map).tolist(), path[2], [], true_map)
            print("I am Fill_List for",elem,"Fill_List",fill_list)
            if(fill_list[0] == True):
                crack_list = crack_list + fill_list[1] + path[2]
                remove_row_col_dupes(crack_list)
    return crack_list

if(0):
    blue_corn = [5,9]
    full_path = path[2]
def is_outside(blue_corn,full_path):
    min_row = min([spec_corner[0] for spec_corner in full_path])
    max_row = max([spec_corner[0] for spec_corner in full_path])
    min_col = min([spec_corner[1] for spec_corner in full_path])
    max_col = max([spec_corner[1] for spec_corner in full_path])

    print("min_row",min_row)
    print("max_row",max_row)
    print("min_col",min_col)
    print("max_col",max_col)
    if(blue_corn[0] <= min_row):
        return True
    if(blue_corn[0] >= max_row):
        return True
    if(blue_corn[1] <= min_col):
        return True
    if(blue_corn[1] >= max_col):
        return True

    return False

#blah = [[2,3],[3,4]]
#blue_corn = [8,8]
#get_corner_blue(elem,true_map)
#get_fill(get_corner_blue(elem,true_map).tolist(),full_path,current_fill,true_map)
#current_fill = []
#blue_corn = [6,7]
#location = [6,7]
#row_col_list = [[9, 7], [9, 7], [9, 8], [9, 7], [9, 8], [9, 9], [9, 7], [9, 8], [9, 9], [8, 9], [9, 7], [9, 8], [9, 9], [8, 9], [7, 9]]

def is_around_blue(location,true_map):
    check_grid = get_nine_grid(location[0],location[1])
    for elem in check_grid:
        if(true_map[elem[0],elem[1]] == BLUE):
            return True
    return False

def remove_row_col_dupes(row_col_list):
    return [list(elem) for elem in list(set([tuple(elem) for elem in row_col_list]))]

def get_fill(blue_corn,full_path,current_fill,true_map):
    print("here",blue_corn)
    if(is_outside(blue_corn,full_path) == False):
        check_grid = get_check_grid(blue_corn[0], blue_corn[1])

        possible_moves = [elem for elem in check_grid if true_map[elem[0], elem[1]] != RED]
        final_moves = [elem for elem in possible_moves if elem not in current_fill]
        if(len(final_moves) == 0):
            copi = copy.copy(current_fill)
            copi.append(blue_corn)

            return True, remove_row_col_dupes(copi)
        else:
            fillup = copy.copy(current_fill)
            fillup.append(blue_corn)
            for elem in final_moves:
                evaluate = get_fill(elem,full_path,fillup,true_map)
                if(evaluate[0] == False):
                    return False, []
                else:
                    fillup = remove_row_col_dupes(fillup + evaluate[1])

            return True, remove_row_col_dupes(fillup)
    else:
        return False,[]

def find_outside(min_row, min_col, max_row, max_col):
    print("how")

# def is_contained_corner():
#     print("contained corner")
# def clear_field():
#     for elem in NODE_ARRAY:
#
#         specific = find_longest_path(elem[1], elem[1], [], circuit_map, elem[0], [])
#         if(specific[0] != -1):
#             corners = [block for block in specific[2] if is_corner(block, elem[0], circuit_map)]
#             min_row = min([spec_corner[0] for spec_corner in corners])
#             max_row = max([spec_corner[0] for spec_corner in corners])
#             min_col = min([spec_corner[1] for spec_corner in corners])
#             max_col = max([spec_corner[1] for spec_corner in corners])

def draw_circuit_stage(donezo):

    neozo= np.zeros((16*40,16*40,3),np.uint8)

    np.place(donezo, donezo <= (BASELINE - 1), 0)

    donezo = donezo - (BASELINE - 1)

    np.place(donezo, donezo == (0 - (BASELINE - 1)), 0)

    print(donezo)
    for i in range(0,donezo.shape[0],1):
        for j in range(0,donezo.shape[1],1):

            if (donezo[i][j] == 0):
                color = (0, 0, 0)
            else:
                if(donezo[i][j]*41 <= 255):

                    color = (255,41 + donezo[i][j]*41,63)
                else:
                    color = (255,61,donezo[i][j]*41 - 255)
            cv2.rectangle(neozo,(0+j*40,0+i*40),(40+j*40,40+i*40),color,-1)



    cv2.imshow("Image",neozo)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def draw_current_stage(donezo):

    neozo= np.zeros((16*40,16*40,3),np.uint8)

    for i in range(0,donezo.shape[0],1):
        for j in range(0,donezo.shape[1],1):

            if(donezo[i][j] == 1):
                color = (255,0,0)
            elif(donezo[i][j] == 3):
                color = (155, 155, 155)
            elif (donezo[i][j] == 2):
                color = (0, 0, 255)
            elif (donezo[i][j] == 5):
                color = (0, 255, 255)
            elif (donezo[i][j] == 4):
                color = (0, 165, 255)
            elif (donezo[i][j] == 0):
                color = (0, 0, 0)
            elif (donezo[i][j] == 6):
                color = (0, 255, 0)

            cv2.rectangle(neozo,(0+j*40,0+i*40),(40+j*40,40+i*40),color,-1)



    cv2.imshow("Image",neozo)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



class Player:
    def __init__(self,row,col):
        self.row = row
        self.col = col
        self.reverse = False
        self.direction= "W"
        self.occupying = False
        self.ring = 0
        self.dead = False
        self.prev_move_turn = False

    def kill(self):
        self.dead = True

    def is_dead(self):
        return self.dead

    def get_prev_move_turn(self):
        return self.prev_move_turn

    def revert_prev_move(self):
        self.prev_move_turn = False

    def increment_ring(self):
        self.ring = (self.ring + 1)

    def get_reverse(self):
        return self.reverse

    def get_occupying(self):
        return self.occupying

    def get_direction(self):
        return self.direction

    def flip_reverse(self):
        if(self.reverse == False):
            self.reverse = True
        else:
            self.reverse = False
    def flip_occupying(self):
        if(self.occupying == False):
            self.occupying = True
        else:
            self.occupying = False
    def set_Position(self,row,col):
        self.row = row
        self.col = col

    def set_direction(self,direction):
        self.direction = direction

    def set_reverse(self,reverse):
        self.reverse = reverse

    def get_Row(self):
        return self.row

    def get_Col(self):
        return self.col

    def position_is_outside(self):
        return is_outside([self.row,self.col],[[-1,-1],[16,16]])

    def turn_left(self):
        if(self.prev_move_turn == True):
            self.kill()

        if(self.direction == "W"):
            self.direction = "S"
        elif(self.direction == "S"):
            self.direction = "E"
        elif(self.direction == "E"):
            self.direction = "N"
        elif(self.direction == "N"):
            self.direction = "W"

        self.prev_move_turn = True

    def jump_one(self):
        self.advance(2)
        self.revert_prev_move()
    def jump_two(self):
        self.advance(3)
        self.revert_prev_move()
    def spring_cap(self):
        self.advance(6)

    def turn_right(self):
        if(self.prev_move_turn == True):
            self.kill()
        else:
            self.revert_prev_move()
        if(self.direction == "W"):
            self.direction = "N"
        elif(self.direction == "N"):
            self.direction = "E"
        elif(self.direction == "E"):
            self.direction = "S"
        elif(self.direction == "S"):
            self.direction = "W"

        self.prev_move_turn = True

    def snap_out_of_it(self):
        if (self.reverse == True):
            self.reverse = False
        else:
            self.dead = True

        self.revert_prev_move()

    def advance(self,length = 1):
        if(self.reverse== False):
            if(self.direction == "W"):
                self.col = self.col - length
            elif(self.direction == "S"):
                self.row = self.row + length
            elif(self.direction == "E"):
                self.col = self.col + length
            elif(self.direction == "N"):
                self.row = self.row - length
        else:
            if (self.direction == "W"):
                self.col = self.col + length
            elif (self.direction == "S"):
                self.row = self.row - length
            elif (self.direction == "E"):
                self.col = self.col - length
            elif (self.direction == "N"):
                self.row = self.row + length

        self.revert_prev_move()

if(0):
    row = 8
    col = 8

def get_check_grid(row,col):
    max_height = donezo.shape[0] - 1
    max_length = donezo.shape[1] - 1
    min_height = 0
    min_length = 0

    check_array = []
    check_array.append([row + 1,col])
    check_array.append([row - 1, col])
    check_array.append([row, col+1])
    check_array.append([row, col-1])
    # for i in range(3):
    #     for j in range(3):
    #         check_array.append([row - 1 + i, col - 1 + j])

    return [elem for elem in check_array if (not (elem[0] == row and elem[1] == col) and
                                            (elem[0] <= max_height and elem[1] <= max_length) and
                                            (elem[0] >= min_length and elem[1] >= min_height))]


def get_nine_grid(row,col):
    max_height = donezo.shape[0] - 1
    max_length = donezo.shape[1] - 1
    min_height = 0
    min_length = 0

    check_array = []
    # check_array.append([row + 1,col])
    # check_array.append([row - 1, col])
    # check_array.append([row, col+1])
    # check_array.append([row, col-1])
    for i in range(3):
        for j in range(3):
            check_array.append([row - 1 + i, col - 1 + j])

    return [elem for elem in check_array if (not (elem[0] == row and elem[1] == col) and
                                            (elem[0] <= max_height and elem[1] <= max_length) and
                                            (elem[0] >= min_length and elem[1] >= min_height))]



def make_slider_corner():
    all_red = [[RED,RED],
     [RED,RED]]

    corner_array = []
    for i in range(len(all_red)):
        for j in range(len(all_red)):
            rando_red = copy.deepcopy(all_red)
            rando_red[i][j] = BLUE
            corner_array.append(rando_red)

    count = 0
    slider_corner = []
    for i in range(-1,1,1):
        for j in range(-1,1,1):
            print("time",j,i)

            slider_corner.append([[i,j],corner_array[count]])
            count = count + 1


    return slider_corner

if(0):
    slider_corner_elem = slider_corner[0]
    location = [4, 8]
    select = 7
    check_corner_type(location, select, circuit_map, slider_corner[3])
def check_corner_type(location,select,circuit_map,slider_corner_elem):
    ok = True
    slider = slider_corner_elem[0]
    corner = slider_corner_elem[1]
    for i in range(len(corner)):
        for j in range(len(corner)):

            print("CircuitMap ", location[0] + slider[0] + i, location[1] + slider[1] + j)
            if(is_outside([location[0] + slider[0] + i, location[1] + slider[1] + j],[[-1,-1],[16,16]]) == False):
                print("CircuitMap ",circuit_map[location[0] + slider[0] +i, location[1] + slider[1] + j])
                print("corna",corner[i][j])



                if(corner[i][j] == 1):

                    if (circuit_map[location[0] + slider[0] +i, location[1] + slider[1] + j] == corner[i][j]):

                        print("passed Check")
                    else:
                        return False
                else:
                    if(circuit_map[location[0] + slider[0] + i, location[1] + slider[1] + j] == corner[i][j]):
                        print("passed Check")
                    elif(circuit_map[location[0] + slider[0] + i, location[1] + slider[1] + j] == select):
                        print("passed Check")

                    else:
                        return False
            else:
                return False
    return ok

if(0):
    location = [6, 9]
    select = 7

    hero = is_corner(location, select, circuit_map)

def is_corner(location,select,circuit_map):
    print("hello")
    slider_corner = make_slider_corner()
    #print(len(slider_corner))
    count = 0
    for elem in slider_corner:
        print("elem",elem)
        print("Neo Kount:",count)
        count = count + 1
        if(check_corner_type(location,select,circuit_map,elem)):
            return True
    return False



def check_around(row,col,circuit_map):
    global MIN_NODE
    global NODE_ARRAY

    check_grid = get_check_grid(row,col)
    check_with_labels = [circuit_map[elem[0],elem[1]] for elem in check_grid]


    if(len([elem for elem in check_with_labels if elem >= BASELINE]) == 0):
        # There is no nodes in the vicinity, time to make a new node
        print("You need to generate Node!",MIN_NODE)
        NODE_ARRAY.append([MIN_NODE, [row, col]])
        MIN_NODE = MIN_NODE + 1

        return [MIN_NODE - 1]



    else:
        #already existing nodes become node
        print("need to recolor nodes")
        return list(set(list([elem for elem in check_with_labels if elem >= BASELINE])))




def paint_circuit(row,col,circuit_map):
    global MIN_NODE
    global NODE_ARRAY
    paints = check_around(row,col,circuit_map)
    if(len(paints) == 1):
        #No need to refill colors only one node in the vicinity
        print("No repainting, single color")
        new_circuit_map = circuit_map.copy()
        new_circuit_map[row,col] = paints[0]


    else:
        if(0):
            paints = [7]
        new_circuit_map = circuit_map.copy()
        new_circuit_map[row, col] = min(paints)
        np.place(new_circuit_map, np.isin(new_circuit_map,paints), min(paints))


    return new_circuit_map



def final_rest(show_map,true_map,playa,initial_row,initial_col,move,circuit_map):
    score = -0.1
    if (playa.is_dead()):
        print("dead")
        return true_map, show_map, initial_row, initial_col, move, circuit_map,score
    elif (playa.position_is_outside()):
        playa.kill()
        print("outside")
        return true_map, show_map, initial_row, initial_col, move, circuit_map,score

    elif ((true_map[playa.get_Row()][playa.get_Col()] == RED) and (playa.get_prev_move_turn() == False)):
        playa.kill()

    elif(true_map[playa.get_Row()][playa.get_Col()] == BLUE):

        circuit_map = paint_circuit(playa.get_Row(),playa.get_Col(),circuit_map)
        true_map[playa.get_Row()][playa.get_Col()] = RED
        score = score + 1

    elif(true_map[playa.get_Row()][playa.get_Col()] == BUMPER):

        if(move == "jump_one"):

            playa.advance(1)
            true_map,show_map,initial_row,initial_col,move,circuit_map,score=final_rest(show_map,true_map,playa,initial_row,initial_col,"adv",circuit_map)

        else:
            playa.set_Position(initial_row,initial_col)
            playa.flip_reverse()
            move = "bounce"


    elif(true_map[playa.get_Row()][playa.get_Col()] == SPRING):


        playa.spring_cap()
        true_map,show_map,initial_row,initial_col,move,circuit_map,score= final_rest(show_map, true_map, playa, initial_row, initial_col, "adv",circuit_map)

    elif(true_map[playa.get_Row()][playa.get_Col()] == RING):
        true_map[playa.get_Row()][playa.get_Col()] = 0
        playa.increment_ring()
        score = score + 2
    show_map = make_show_map(true_map, playa)

    return true_map,show_map,initial_row,initial_col,move,circuit_map,score






def convert_position_from_prime(row,col):
    return 2**row*3**col

if(0):
    row = 2
    col = 4
    cur_position = [4,10]
    node_num = 1
    previous_moves_encrypt = []
    end_location = [4,10]
    prev_move = []
    cur_position = NODE_ARRAY[0][1]

    bah = [[4,5],[5,6]]
    bah = bah + [[4,1]]
    find_longest_path(cur_position,cur_position,[],circuit_map,NODE_ARRAY[0][0],[])


    find_longest_path(NODE_ARRAY[0][1], NODE_ARRAY[0][1], [], circuit_map, NODE_ARRAY[0][0], [])



def find_longest_path(cur_position,end_location,previous_moves_encrypt,circuit_map,node_num,prev_move):
    print("hi")
    print("Current",cur_position)
    turn = len(previous_moves_encrypt)

    if(not is_around_blue(cur_position,true_map)):
        return -1, previous_moves_encrypt, prev_move

    if((turn == 2) and convert_position_from_prime(cur_position[0],cur_position[1])
            == convert_position_from_prime(end_location[0],end_location[1])):
        return -1,previous_moves_encrypt,prev_move
    elif((turn > 2) and convert_position_from_prime(cur_position[0],cur_position[1])
            == convert_position_from_prime(end_location[0],end_location[1])):
        return turn,previous_moves_encrypt,prev_move

    else:

        check_grid = get_check_grid(cur_position[0],cur_position[1])

        possible_moves = [elem for elem in check_grid if circuit_map[elem[0],elem[1]] == node_num]
        final_moves = [elem for elem in possible_moves if
                          (not convert_position_from_prime(elem[0],elem[1])  in previous_moves_encrypt) ]
        evaluate_array = []
        print("final",final_moves)
        print("possible moves:",possible_moves)
        print(len(final_moves))
        if (len(final_moves) == 0):
            return -1,previous_moves_encrypt,prev_move
        else:
            print("Made it here")
            for elem in final_moves:
                copi = copy.copy(prev_move)
                copi.append(elem)
                evaluate_array.append(find_longest_path(elem,end_location,
                                  previous_moves_encrypt+ [convert_position_from_prime(elem[0],elem[1])],circuit_map,node_num,copi))


            max_length = -1
            trail = []
            clear_trail = []

            for elem in evaluate_array:
                if (elem[0] > max_length):
                    max_length = elem[0]
                    trail = elem[1]
                    clear_trail = elem[2]

            return max_length,trail,clear_trail


if(0):
    find_shortest_path(elem, elem, [], true_map, RED, [])
    cur_position = elem
    end_location = elem
    previous_moves_encrypt = []
    circuit_map = true_map
    node_num = RED
    prev_move = []
def find_shortest_path(cur_position,end_location,previous_moves_encrypt,circuit_map,node_num,prev_move):
    print("hi")
    print("Current",cur_position)
    turn = len(previous_moves_encrypt)
    print("I am turn",turn)

    if(not is_around_blue(cur_position,true_map)):
        return -1, previous_moves_encrypt, prev_move

    if((turn == 2) and convert_position_from_prime(cur_position[0],cur_position[1])
            == convert_position_from_prime(end_location[0],end_location[1])):
        return -1,previous_moves_encrypt,prev_move
    elif((turn > 2) and convert_position_from_prime(cur_position[0],cur_position[1])
            == convert_position_from_prime(end_location[0],end_location[1])):
        return turn,previous_moves_encrypt,prev_move

    else:

        check_grid = get_check_grid(cur_position[0],cur_position[1])

        possible_moves = [elem for elem in check_grid if circuit_map[elem[0],elem[1]] == node_num]
        final_moves = [elem for elem in possible_moves if
                          (not convert_position_from_prime(elem[0],elem[1])  in previous_moves_encrypt) ]
        evaluate_array = []
        print("final",final_moves)
        print("possible moves:",possible_moves)
        print(len(final_moves))
        if (len(final_moves) == 0):
            return -1,previous_moves_encrypt,prev_move
        else:
            print("Made it here")
            for elem in final_moves:
                copi = copy.copy(prev_move)
                copi.append(elem)
                evaluate_array.append(find_shortest_path(elem,end_location,
                                  previous_moves_encrypt+ [convert_position_from_prime(elem[0],elem[1])],circuit_map,node_num,copi))


            min_length = 1000000
            trail = []
            clear_trail = []

            for elem in evaluate_array:
                if ((elem[0] < min_length) & (elem[0] != -1)):
                    min_length = elem[0]
                    trail = elem[1]
                    clear_trail = elem[2]

            if(len(trail) == 0):
                min_length = -1
            return min_length,trail,clear_trail


def convert_ensnare(ensnare,true_map,playa):
    bonus_points = 0
    if(len(ensnare) >= 0):

        if(len(ensnare) <= 9):
            bonus_points = len(ensnare)*1.2
        elif(len(ensnare) <= 16):
            bonus_points = len(ensnare)*1.5
        else:
            bonus_points = len(ensnare) * 2

        for elem in ensnare:
            true_map[elem[0]][elem[1]] = RING

    if (playa.position_is_outside() == False):
        if(true_map[playa.get_Row()][playa.get_Col()] == RING):
            true_map[playa.get_Row()][playa.get_Col()] = 0

    return true_map,bonus_points

def make_show_map(true_map,playa):
    show_map =copy.copy(true_map)
    if(playa.position_is_outside() == False):
        show_map[playa.get_Row()][playa.get_Col()] = 6
        return show_map
    else:
        return show_map


def evaluate_move(show_map,true_map,move,playa):
    initial_row = playa.get_Row()
    initial_col = playa.get_Col()

    final_move = ""
    #set_flag= False
    if(move == "adv"):
        playa.advance(1)



        # if(map[playa.get_Row()][playa.get_Col()] == 3):
        #     playa.advance(-1)
        #     playa.flip_reverse()
        #
        #     final_move = "bounce"
        #     set_flag = True
        #     #return "bounce"
        #
        # else:
        #     final_move = "adv"
        # #return "adv"

    elif((move == "left") ):
        playa.turn_left()
        final_move =  "left"


    elif(move == "right" ):
        playa.turn_right()
        final_move =  "right"


    elif(move == "snap"):
        playa.snap_out_of_it()
        # if(map[playa.get_Row()][playa.get_Col()] == 3):
        #     playa.advance(-1)
        #     playa.flip_reverse()
        #     final_move = "bounce"
        # else:
        #
        #     final_move =  "reversi"
        #

    elif(move == "jump_one"):

        playa.jump_one()

        # if (map[playa.get_Row()][playa.get_Col()] == 3):
        #     playa.advance(1)
        #  um   if(map[playa.get_Row()][playa.get_Col()] == 3):
        #         playa.set_Position(initial_row,initial_col)
        #         playa.advance(-1)
        #         playa.flip_reverse()
        #         final_move =  "bounce"
        #     else:
        #
        #         final_move =  "jump_one"

    elif(move == "jump_two"):
        playa.jump_two()

        # if(map[playa.get_Row()][playa.get_Col()] == 3):
        #     playa.set_Position(initial_row, initial_col)
        #     playa.advance(-1)
        #     playa.flip_reverse()
        #     final_move =  "bounce"
        # else:
        #     final_move =  "jump_two"

    return final_rest(show_map,true_map,playa,initial_row,initial_col,move,circuit_map)


blue_spheres_saves_location = ".//Blue_Spheres_Data//"
spooky= os.listdir(blue_spheres_saves_location)
print(spooky)
len(spooky)
i = 4
print(spooky[i])
donezo =np.load(blue_spheres_saves_location+spooky[i])


true_map = copy.copy(donezo)

circuit_map = copy.copy(donezo)

np.place(true_map, true_map == 6, 0)

draw_current_stage(donezo)

map = donezo
playa = Player(3,15)

show_map = map

#for i in range(0,20,1):

typing = ""

while(typing != "done"):
    print("Direction:",playa.get_direction())
    print("Reverse:",playa.get_reverse())
    typing = input("Next Move:")
    if(typing== ""):
        typing= "adv"
    true_map,show_map,initial_row,initial_col,move,circuit_map,score = evaluate_move(show_map,true_map,typing,playa)

    print("I will ensare")
    true_map, bonus_points = convert_ensnare(neo_ensnare(true_map),true_map,playa)
    show_map = make_show_map(true_map,playa)
    draw_current_stage(show_map)
    print("I am the circuit map",circuit_map)
    fake_circ = copy.copy(circuit_map)
    #draw_circuit_stage(fake_circ)
    full_score = score + bonus_points

    if(playa.is_dead()):
        print("I AM DEAD")
        typing= "done"
        full_score = -10


    print("Full_Score",full_score)
    np.array(show_map)


# blah = np.count_nonzero((true_map == 1) | (true_map == 5))
np.linalg.norm(np.array(np.array([0,0])) - np.array([15,3]))