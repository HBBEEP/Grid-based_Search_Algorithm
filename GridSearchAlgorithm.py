import numpy as np
import math

class GridSearchAlgorithm:
    def __init__(self, rows: int, columns: int, walls: list, target_pos: tuple, init_pos: tuple) -> None:

        self.map_reset(rows, columns, walls, target_pos, init_pos)

    def create_map(self):
        map_array = np.full((self.rows, self.columns), '.', dtype=str)
        map_array[self.target_pos[0], self.target_pos[1]] = 'T'
        map_array[self.init_pos[0], self.init_pos[1]] = 'I'
        for wall in self.walls:
            if 0 <= wall[0] < self.rows and 0 <= wall[1] < self.columns:
                map_array[wall[0], wall[1]] = '|'
        return map_array

    def map_reset(self, rows, columns, walls, target_pos, init_pos):
        self.rows = rows
        self.columns = columns
        self.walls = walls
        self.target_pos = target_pos
        self.init_pos = init_pos

        self.map = self.create_map()

        self.Q = []
        self.Q.append(self.init_pos)
        self.state_status = {self.init_pos : '1'}
        self.path = {}

        self.f_cost = {self.init_pos : self.cal_euclidean_distance(self.init_pos, self.target_pos)}
        self.g_cost = {self.init_pos : 0}
        self.close = []


    def get_neighbors(self, x_current):
        U = [(1,0),(-1,0),(0,-1),(0,1),(1,1),(-1,1),(1,-1),(-1,-1)]
        ret = []
        for u in U:
            x_new = (x_current[0] + u[0], x_current[1] + u[1])
            if  0 <= x_new[0] < self.rows and 0 <= x_new[1] < self.columns and (self.map[x_new] == '.' or self.map[x_new] == 'T'):
                ret.append(x_new)
        return ret
    
    def get_path(self, paths):
        ret = []
        x = self.target_pos
        while x != self.init_pos:
            ret.append(x)
            x = paths[x]
        ret.append(x)
        ret.pop(0)
        return ret

    def breath_first_search(self):
        path_map = None
        if self.Q!= []: #loop
            x = self.Q.pop(0)
            self.state_status[x] = '2'
            current_cost = self.g_cost[x]
            if x == self.target_pos:
                path_map  = self.get_path(self.path)
                return self.state_status, path_map, current_cost 
            for x_new in self.get_neighbors(x):
                cost_to_come_next = current_cost + self.cal_euclidean_distance(x, x_new)
                if (self.state_status.get(x_new) is None):
                    self.path[x_new] = x
                    self.state_status[x_new] = '1'
                    self.Q.append(x_new)
                    self.g_cost[x_new] = cost_to_come_next

        return self.state_status, path_map, current_cost 

    def a_star_search(self):
        path_map = None
        current_cost = None
        if self.Q!= []: #loop

            lowest_f_index = 0

            for i in range(len(self.Q)):
                if self.f_cost[self.Q[i]] <  self.f_cost[self.Q[lowest_f_index]]:
                    lowest_f_index = i
            low_cost = self.Q[lowest_f_index]
            min_index = self.Q.index(low_cost) 

            x = self.Q.pop(min_index)
            self.close.append(x)
            current_cost = self.g_cost[x]

            self.state_status[x] = '2'
            if x == self.target_pos:
                path_map  = self.get_path(self.path)
                return self.state_status, path_map, current_cost 


            for x_new in self.get_neighbors(x):
                if x_new not in self.close:
                    new_path = False
                    cost_to_come_next = current_cost + self.cal_euclidean_distance(x, x_new)
                    cost_to_go_next =  self.cal_euclidean_distance(x_new, self.target_pos) 

                    if x_new in self.Q:
                        self.state_status[x_new] = '1'

                        if (cost_to_come_next < self.g_cost[x_new]):

                            self.g_cost[x_new] = cost_to_come_next
                            new_path = True
                    else:
                        self.g_cost[x_new] = cost_to_come_next
                        new_path = True
                        self.Q.append(x_new)

                    if (new_path):

                        self.path[x_new] = x
                        self.f_cost[x_new] =  cost_to_go_next + cost_to_come_next

        return self.state_status, path_map , current_cost 
            
    def best_first_search(self):
        path_map = None
        current_cost = None

        if self.Q!= []: #loop

            lowest_f_index = 0

            for i in range(len(self.Q)):
                if self.f_cost[self.Q[i]] <  self.f_cost[self.Q[lowest_f_index]]:
                    lowest_f_index = i
            low_cost = self.Q[lowest_f_index]
            min_index = self.Q.index(low_cost) 

            x = self.Q.pop(min_index)
            self.close.append(x)
            current_cost = self.g_cost[x]

            self.state_status[x] = '2'
            if x == self.target_pos:
                path_map  = self.get_path(self.path)
                return self.state_status, path_map, current_cost 


            for x_new in self.get_neighbors(x):
                if x_new not in self.close:
                    new_path = False
                    cost_to_come_next = current_cost + self.cal_euclidean_distance(x, x_new)
                    cost_to_go_next =  self.cal_euclidean_distance(x_new, self.target_pos) 

                    if x_new in self.Q:
                        self.state_status[x_new] = '1'

                        if (cost_to_come_next < self.g_cost[x_new]):

                            self.g_cost[x_new] = cost_to_come_next
                            new_path = True
                    else:
                        self.g_cost[x_new] = cost_to_come_next
                        new_path = True
                        self.Q.append(x_new)

                    if (new_path):

                        self.path[x_new] = x
                        self.f_cost[x_new] =  cost_to_go_next 

        return self.state_status, path_map, current_cost 

    def get_map(self)->list:
        return self.map
    
    def cal_euclidean_distance(self, current_pos, target_pos)->int:
        return math.sqrt((target_pos[0] - current_pos[0])**2 + (target_pos[1] - current_pos[1])**2)
             
    def cal_manhattan_distance(self, current_pos, target_pos)->int:
        return abs(target_pos[0] - current_pos[0]) + abs(target_pos[1] - current_pos[1])
         