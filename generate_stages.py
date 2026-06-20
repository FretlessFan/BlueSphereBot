import os
import numpy as np
import copy
import datetime as dt

# BLUE = 1
# RED = 2
# BUMPER = 3
# SPRING = 4
# RING = 5
# PLAYER = 6

class Blue_Generator():
    def __init__(self,chunks,stage_names="Random_Generated",number=10,
                 location="C://Users//wsreees//Downloads//moon//gym_examples//envs//"):
        self.chunks = chunks
        self.number = number
        self.stage_names = stage_names
        self.location = location
        os.makedirs(location + stage_names, exist_ok=True)

    def is_done(self,current_chunks):
        return sum([elem["num"] for elem in current_chunks]) == 0

    def will_fit(self,selected_chunk,row_place,col_place):
        if (np.array(selected_chunk["chunk"]).shape[0] + row_place > 15):
            return False

        if (np.array(selected_chunk["chunk"]).shape[1] + col_place > 15):
            return False

        return True
    if(0):
        current_chunks = [{"num":5,"chunk":[[RING]]},{"num":5,"chunk":[[BLUE,BLUE],
                                                                      [BLUE,BLUE]]}]


    def generate(self,generate_number=None,save=True):
        if(generate_number!=None):
            print("Generating stage:",generate_number)

        grid = np.zeros((16,16))

        current_chunks = copy.deepcopy(self.chunks)

        while(not self.is_done(current_chunks)):
            selected_value = False
            while (selected_value == False):
                selection = np.random.randint(0, len(current_chunks))
                if(current_chunks[selection]["num"]!=0):
                    selected_value = True

            selected_chunk = current_chunks[selection]

            placed = False
            while(not placed):
                row_place = np.random.randint(0, grid.shape[0])
                col_place = np.random.randint(0, grid.shape[0])

                if (self.will_fit(selected_chunk,row_place,col_place)):
                    np_chunk= np.array(selected_chunk["chunk"])
                    for i in range(np_chunk.shape[0]):
                        for j in range(np_chunk.shape[1]):
                            grid[i+row_place][j+col_place] = np_chunk[i][j]
                    placed = True
                    current_chunks[selection]["num"] -= 1

        row_place = np.random.randint(0, 14)
        col_place = np.random.randint(0, grid.shape[0])


        grid[3][15] = 0
        grid[15][3] = 0
        grid[row_place][col_place] = 6

        if(save):
            if(generate_number!=None):

                np.save(self.location + "/" + self.stage_names + "/" + self.stage_names +str(generate_number) + ".npy", grid)
            else:
                np.save(self.location + "/" + self.stage_names + "/" + self.stage_names + str(dt.datetime.now()).replace(
                    "-","_").replace(" ","_").replace(":","_").replace(".","_")+".npy",
                        grid)

        return grid

# stage_names = "Random_Generated"
# location= "C://Users//wsreees//Downloads//moon//gym_examples//envs//"
# os.makedirs(location+stage_names, exist_ok=True)
# blue = Blue_Generator(current_chunks)
#
# grid=blue.generate()