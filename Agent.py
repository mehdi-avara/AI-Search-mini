from Environment import Board
import colors
class Agent:
    def __init__(self, board, clock,FPS):
        self.position = board.get_agent_pos()
        self.current_state = board.get_current_state()
        self.board = board
        self.clock = clock
        self.FPS = FPS


    def get_position(self):
        return self.position

    def set_position(self, position, board):
        self.position = position
        board.set_agent_pos(position)
        board.update_board(self.current_state)

    def percept(self, board):
        # perception :
        # sets the current state
        # Use get_current_state function to get the maze matrix. - make your state
        self.current_state = board.get_current_state()
        self.position = board.get_agent_pos()

        pass
    def check(self, direction,current):
        actions = self.get_actions(self)
        if not(direction in actions):
            return
        new_Pos = ((current[0] + direction[0]),(current[1] + direction[1]))
        x, y = new_Pos[0], new_Pos[1]
        self.board.colorize(x, y, colors.red)


    def move(self, direction):
        # make your next move based on your perception
        # check if the move destination is not blocked
        actions = self.get_actions(self)
        if not(direction in actions):
            return
        # if not blocked:
        # use red color to show visited tiles.
        # something like :
        current_pos = self.get_position()
        x, y = current_pos[0], current_pos[1]
        self.board.colorize(x, y, colors.green)
        # then move to destination - set new position
        # something like :
        new_Pos = ((self.get_position()[0] + direction[0]),(self.get_position()[1] + direction[1]))
        self.set_position({'x':new_Pos[0],'y':new_Pos[1]},self.board)

        pass

    @staticmethod
    def get_actions(self):
        actions = []
        self.position = self.board.get_agent_pos()
        if not Agent.is_up_block(self.position,self.board):
            actions.append((0,-1))
        if not Agent.is_down_block(self.position,self.board):
            actions.append((0,1))
        if not Agent.is_right_block(self.position,self.board):
            actions.append((1,0))
        if not Agent.is_left_block(self.position,self.board):
            actions.append((-1,0))
        return actions
    def get_actions(self,pos):
        actions = []
        if not Agent.is_right_block(pos,self.board):
            actions.append((1,0))
        if not Agent.is_up_block(pos,self.board):
            actions.append((0,-1))
        if not Agent.is_down_block(pos,self.board):
            actions.append((0,1))
        if not Agent.is_left_block(pos,self.board):
            actions.append((-1,0))
        return actions
    def is_right_block(pos,board):
        current_state = board.get_current_state()
        if pos[0] >= len(current_state)-1:
            return True
        return current_state[pos[0]+1][pos[1]].is_blocked()
    def is_left_block(pos,board):
        current_state = board.get_current_state()
        if pos[0] <=0:
            return True
        return current_state[pos[0]-1][pos[1]].is_blocked()
    def is_up_block(pos,board):
        current_state = board.get_current_state()
        if pos[1] <=0:
            return True
        return current_state[pos[0]][pos[1]-1].is_blocked()
    def is_down_block(pos,board):
        current_state = board.get_current_state()
        if pos[1] >= (len(current_state[0])-1):
            return True
        return current_state[pos[0]][pos[1]+1].is_blocked()
    def bfs(self):
        way_out = False
        open_list = []
        visited = []
        open_list.append(Tree_node(None,self.position))
        while len(open_list)!=0:
            father = open_list[0]
            open_list.pop(0)
            visited.append(father.data)
            if father.data == self.board.goal_pos:
                way_out = self.found(Tree_node(father,new_point))
                break
            self.paint(father.data,colors.red)
            actions = self.get_actions(father.data)
            for i in actions:
                new_point  = (i[0]+father.data[0], i[1]+father.data[1])
                if new_point in visited:
                    continue
                open_list.append(Tree_node(father,new_point))
                self.paint(new_point,colors.black)
        if way_out==False:
            print("no way out")
            return

    def paint(self,point,color):
            x, y = point[0], point[1]
            self.board.colorize(x, y, color) 
            self.clock.tick(self.FPS)
            self.board.draw_world()
    def found(self,end):
        while not (end.father==None):
            self.paint(end.data,colors.green)
            end = end.father
        self.paint(end.data,colors.green)
        return True
        
    def dfs(self):
        visited_list = []
        way_out = []
        way_out.append(self.position)
        self.paint(self.position,colors.black)
        if self.dfs_recurcive(way_out,visited_list,self.position) == True:
            for i in way_out:
                self.paint(i,colors.green)
        else:
            print("no way out")

    def dfs_recurcive(self,way,visited,point):
        if point == self.board.goal_pos:
            return True
        visited.append(point)
        self.paint(point,colors.red)
        available_moves = self.get_actions(point)
        for i in available_moves:
            new_pos = (point[0]+i[0],point[1]+i[1])
            if new_pos in visited:
                continue
            self.paint(point,colors.black)
            visited.append(new_pos)
            way.append(new_pos)
            if self.dfs_recurcive(way,visited,new_pos):
                return True
            way.pop()
        return False
    def a_star(self):
        way_out = []
        way_out.append(self.position)
        self.paint(self.position,colors.black)
        fewest_distance = self.a_star_recursive(9223372036854775807,self.position,0,way_out)
        if  fewest_distance == 0:
            for i in way_out:
                self.paint(i,colors.green)
        else:
            print("no way out")
    def a_star_recursive(self,fewest,point,distance_from_start,way_out):
        if point == self.board.goal_pos:
            return 0
        self.paint(point,colors.red)
        available_moves = self.get_actions(point)
        available_moves_cost = []
        for i in available_moves:
            new_pos = (point[0]+i[0],point[1]+i[1],(self.heuristic((point[0]+i[0],point[1]+i[1]))+distance_from_start))    
            available_moves_cost.append(new_pos)
            self.paint(point,colors.black)
        available_moves_cost.sort(key =lambda num: num[2])

        print(available_moves_cost)
        while available_moves_cost[0][2]<=fewest:
            holder = (available_moves_cost[0][0],available_moves_cost[0][1])
            way_out.append(holder)
            if available_moves_cost[0][2]==0:
                return 0
            elif(len(available_moves_cost)>=2):
                available_moves_cost[0] = (available_moves_cost[0][0],available_moves_cost[0][1],self.a_star_recursive(min(fewest,available_moves_cost[1][2]),holder,distance_from_start+1,way_out))
            elif(len(available_moves_cost)==1):
                available_moves_cost[0] = (available_moves_cost[0][0],available_moves_cost[0][1],self.a_star_recursive(fewest,holder,distance_from_start+1,way_out))
            else:
                return 9223372036854775807
            way_out.pop()
            available_moves_cost = sorted(available_moves_cost,key= lambda num: num[2])
        return available_moves_cost[0][2]
    # def a_star(self):
    #     pass
    def heuristic(self,position):
        x,y=position[0],position[1]
        goal = self.board.goal_pos
        return (abs(x-goal[0])+abs(y-goal[1]))
    
    def a_star(self):
        way_out = False
        open_list = []
        visited = []
        open_list.append((Tree_node(None,self.position),self.heuristic(self.position)))
        while len(open_list)!=0:
            father = open_list[0][0]
            open_list.pop(0)
            visited.append(father.data)
            if father.data == self.board.goal_pos:
                way_out = self.found(Tree_node(father,new_point))
                break
            self.paint(father.data,colors.red)
            actions = self.get_actions(father.data)
            for i in actions:
                new_point  = (i[0]+father.data[0], i[1]+father.data[1])
                if new_point in visited:
                    continue
                open_list.append((Tree_node(father,new_point),self.heuristic(new_point)))
                self.paint(new_point,colors.black)
            open_list.sort(key= lambda num : num[1])
        if way_out==False:
            print("no way out")
            return
 
class Tree_node:
    def __init__(self,father,data):
        self.father = father
        self.data = data

    def get_data(self):
        return self.data
    def get_father(self):
        return self.father