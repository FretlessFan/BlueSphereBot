import cv2

import numpy as np
import os
import copy


#true_map = donezoj

if(0):
    for i in range(4,7,1):
        for j in range(8,11,1):

            true_map[i][j] = 7
            if(i == 5 and j==9):
                true_map[i][j] = 1

import pandas as pd
def find_surrounding(true_map):

    indic = np.where(true_map == 7)

    rows= indic[0]
    columns = indic[1]

    all_pos= pd.DataFrame()
    all_pos["rows"] =rows
    all_pos["cols"] = columns

    elems= all_pos.values.tolist()

    bubble_list = []

    #tuple(elems)
    for elem in elems:
        bubble_list.append((elem[0],elem[1]))

    list(set(bubble_list))


    kool_dict =dict()
    #set(elems)
    #i = 0


    for i in range(0,len(bubble_list),1):
        part_row=bubble_list[i][0]
        part_col =bubble_list[i][1]

        location = all_pos[ (part_row-1 <= all_pos["rows"]) & (part_row+1 >= all_pos["rows"])  & (all_pos["cols"] >= part_col-1) & (all_pos["cols"] <= part_col+1)
                            &((all_pos["rows"] != part_row) | (all_pos["cols"] != part_col)) & ((abs(all_pos["cols"] -part_col) +abs(all_pos["rows"] -part_row))== 1)  ]


        complete = []
        for elem in location.values.tolist():
            complete.append(tuple(elem))
        kool_dict[bubble_list[i]] = complete


    finished_list= []
    queue = []
    explored_list = []

    neodone = False
    while(len(list(set(list(kool_dict.keys()))- set(explored_list)))!=0):
    #while(neodone == False):
        start = list(set(list(kool_dict.keys()))- set(explored_list))[0]
        queue.append(start)
        j  = 0

        while(len(queue) != 0):
            print("queue",queue)
            v = queue.pop()
            print("v:",v)
            print("current j:",j)

            for elem in kool_dict[v]:
                if ((elem in explored_list)==False):
                    print("exploredList:",explored_list)
                    print("elem:",elem)

                    if((elem == start) & (j >= 7)):
                        print("we did it!")
                        finished_list.append(start)
                        explored_list.append(elem)
                    if( (elem != start)):
                        explored_list.append(elem)

                        queue.append(elem)

            j = j+1
        #neodone=True







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

            elif (donezo[i][j] == 7):
                color = (0, 0, 180)

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

    def turn_left(self):
        if(self.direction == "W"):
            self.direction = "S"
        elif(self.direction == "S"):
            self.direction = "E"
        elif(self.direction == "E"):
            self.direction = "N"
        elif(self.direction == "N"):
            self.direction = "W"

    def jump_one(self):
        self.advance(2)
    def jump_two(self):
        self.advance(3)

    def spring_cap(self):
        self.advance(6)

    def turn_right(self):
        if(self.direction == "W"):
            self.direction = "N"
        elif(self.direction == "N"):
            self.direction = "E"
        elif(self.direction == "E"):
            self.direction = "S"
        elif(self.direction == "S"):
            self.direction = "W"

    def snap_out_of_it(self):
        if (self.reverse == True):
            self.reverse = False
        else:
            self.advance(1)

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




def final_rest(show_map,true_map,playa,initial_row,initial_col,move):
    if(true_map[playa.get_Row()][playa.get_Col()] == 1):

        true_map[playa.get_Row()][playa.get_Col()] = 7

    elif(true_map[playa.get_Row()][playa.get_Col()] == 3):

        if(move == "jump_one"):

            playa.advance(1)
            true_map,show_map,initial_row,initial_col,move=final_rest(show_map,true_map,playa,initial_row,initial_col,"adv")

        else:
            playa.set_Position(initial_row,initial_col)
            playa.flip_reverse()
            move = "bounce"


    elif(true_map[playa.get_Row()][playa.get_Col()] == 4):


        playa.spring_cap()
        true_map,show_map,initial_row,initial_col,move= final_rest(show_map, true_map, playa, initial_row, initial_col, "adv")

    elif(true_map[playa.get_Row()][playa.get_Col()] == 5):
        true_map[playa.get_Row()][playa.get_Col()] = 0



    show_map =copy.copy(true_map)
    show_map[playa.get_Row()][playa.get_Col()] = 6

    return true_map,show_map,initial_row,initial_col,move

            #true_map[playa.get_Row()][playa.get_Col()] = 2

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

    elif(move == "left"):
        playa.turn_left()
        final_move =  "left"

    elif(move == "right"):
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

    return final_rest(show_map,true_map,playa,initial_row,initial_col,move)


spooky= os.listdir("C://Users//jzbus//Downloads//Blue_Spheres_Data//Blue_Spheres_Data//")
i = 0
print(spooky[i])
donezo =np.load("C://Users//jzbus//Downloads//Blue_Spheres_Data//Blue_Spheres_Data//"+spooky[i])


true_map = copy.copy(donezo)
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
    true_map,show_map,initial_row,initial_col,move = evaluate_move(show_map,true_map,typing,playa)

    draw_current_stage(show_map)



