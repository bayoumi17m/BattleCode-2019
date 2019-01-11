from random import *
import util


coord_to_dir = {
    (0,0): "C",
    (0,1): "S",
    (1,1): "SE",
    (1,0): "E",
    (1,-1): "NE",
    (0,-1): "N",
    (-1, -1): "NW",
    (-1, 0): "W",
    (-1, 1): "SW",
}

dir_to_coord = {
    "C": (0,0),
    "S": (0,1),
    "SE": (1,1),
    "E": (1,0),
    "NE": (1,-1),
    "N": (0,-1),
    "NW": (-1, -1),
    "W": (-1, 0),
    "SW": (-1, 1),   
}

def calculate_dir(start, target):
    """
    Calculate the direction in which to go to get from start to target.
    start: a tuple representing an (x,y) point
    target: a tuple representing an (x,y) point
    as_coord: whether you want a coordinate (-1,0) or a direction (S, NW, etc.)
    """
    dx = target[0] - start[0]
    dy = target[1] - start[1]
    if dx < 0:
        dx = -1
    elif dx > 0:
        dx = 1
    
    if dy < 0:
        dy = -1
    elif dy > 0: 
        dy = 1
    
    return (dx, dy)

rotate_arr = [    
    (0,1),
    (1,1),
    (1,0),
    (1,-1),
    (0,-1),
    (-1, -1),
    (-1, 0),
    (-1, 1)
]

def get_list_index(lst, tup):
    # only works for 2-tuples
    for i in range(len(lst)):
        if lst[i][0] == tup[0] and lst[i][1] == tup[1]:
            return i

def rotate(orig_dir, amount):
    direction = rotate_arr[(get_list_index(rotate_arr, orig_dir) + amount) % 8]
    return direction

def reflect(full_map, loc, horizontal=True):
    #need to use len-1 not len as a 57x57 board will only go up to a tile 56, start on that the h mirror should be zero
    v_reflec = (len(full_map[0])-1 - loc[0], loc[1])
    h_reflec = (loc[0], len(full_map)-1 - loc[1])
    if horizontal:
        return h_reflec if full_map[h_reflec[1]][h_reflec[0]] else v_reflec
    else:
        return v_reflec if full_map[v_reflec[1]][v_reflec[0]] else h_reflec

def is_passable(full_map, loc, coord_dir, robot_map=None):
    new_point = (loc[0] + coord_dir[0], loc[1] + coord_dir[1])
    if new_point[0] < 0 or new_point[0] > len(full_map):
        return False
    if new_point[1] < 0 or new_point[0] > len(full_map):
        return False
    if not full_map[new_point[1]][new_point[0]]:
        return False
    if robot_map is not None and robot_map[new_point[1]][new_point[0]] > 0:
        return False
    return True

def apply_dir(loc, dir):
    return (loc[0] + dir[0], loc[1] + dir[1])

def goto(loc, target, full_map, robot_map, already_been):
    goal_dir = calculate_dir(loc, target)
    if goal_dir is (0,0):
        return (0,0)
    # self.log("MOVING FROM " + str(my_coord) + " TO " + str(nav.dir_to_coord[goal_dir]))
    i = 0
    while not is_passable(full_map, loc, goal_dir, robot_map) and i < 4:# or apply_dir(loc, goal_dir) in already_been: # doesn't work because `in` doesn't work :(
        # alternate checking either side of the goal dir, by increasing amounts (but not past directly backwards)
        if i > 0:
            i = -i
        else:
            i = -i + 1
        goal_dir = rotate(goal_dir, i)
    return goal_dir




        


# def goto(loc, target, full_map, robot_map, already_been):
#     goal_dir = calculate_dir(loc, target)
#     if goal_dir is (0,0):
#         return (0,0)
#     #self.log("MOVING FROM " + str(my_coord) + " TO " + str(nav.dir_to_coord[goal_dir]))
#     #while (not is_passable(full_map, loc, goal_dir, robot_map)) or (apply_dir(loc, goal_dir) in already_been):
#     target=apply_dir(loc, goal_dir)
#     # while (not is_passable(full_map, loc, goal_dir, robot_map)) or (apply_dir(loc, goal_dir) in already_been):
#     #     goal_dir = rotate(goal_dir, 1)
#     #     target=apply_dir(loc, goal_dir)
#     return goal_dir
    
   



def get_closest_karbonite(loc, karb_map):
    closest_karb = (-100, -100)
    karb_dist_sq = 100000
    for x in range(len(karb_map)):
        if abs(x - loc[0]) > karb_dist_sq:
            break
        for y in range(len(karb_map)):
            if abs(y - loc[1]) > karb_dist_sq:
                break
            if karb_map[y][x] and sq_dist((x,y), loc) < karb_dist_sq:
                karb_dist_sq = sq_dist((x,y), loc)
                closest_karb = (x,y)
    return closest_karb

def sq_dist(p1, p2):
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

def spawn(loc,full_map,robot_map):
    goal_dir=(-1,0)
    while not is_passable(full_map, loc, goal_dir, robot_map):
        goal_dir = rotate(goal_dir, 1)
    
    return goal_dir

def symmetric(full_map):
    l=len(full_map)

    coord1=randint(0,l),randint(0,l)
    coord1_h=coord1[0],l-1-coord1[1]
    coord2=randint(0,l),randint(0,l)
    coord2_h=coord2[0],l-1-coord2[1]
    coord3=randint(0,l),randint(0,l)
    coord3_h=coord3[0],l-1-coord3[1]
    coord4=randint(0,l),randint(0,l)
    coord4_h=coord4[0],l-1-coord4[1]
    coord5=randint(0,l),randint(0,l)
    coord5_h=coord5[0],l-1-coord5[1]
    coord6=randint(0,l),randint(0,l)
    coord6_h=coord6[0],l-1-coord6[1]
    coord7=randint(0,l),randint(0,l)
    coord7_h=coord7[0],l-1-coord7[1]
    coord8=randint(0,l),randint(0,l)
    coord8_h=coord8[0],l-1-coord8[1]
    coord9=randint(0,l),randint(0,l)
    coord9_h=coord9[0],l-1-coord9[1]
    coord10=randint(0,l),randint(0,l)
    coord10_h=coord10[0],l-1-coord10[1]


    while full_map[coord1[1]][coord1[0]]:
        coord1=randint(0,l),randint(0,l)
    coord1_h=coord1[0],l-1-coord1[1]
    while full_map[coord2[1]][coord2[0]]:
        coord2=randint(0,l),randint(0,l)
    coord2_h=coord2[0],l-1-coord2[1]
    while full_map[coord3[1]][coord3[0]]:
        coord3=randint(0,l),randint(0,l)
    coord3_h=coord3[0],l-1-coord3[1]
    while full_map[coord4[1]][coord4[0]]:
        coord4=randint(0,l),randint(0,l)
    coord4_h=coord4[0],l-1-coord4[1]




    if full_map[coord1_h[1]][coord1_h[0]]==full_map[coord1[1]][coord1[0]]:
        if full_map[coord2_h[1]][coord2_h[0]]==full_map[coord2[1]][coord2[0]]:
            if full_map[coord3_h[1]][coord3_h[0]]==full_map[coord3[1]][coord3[0]]:
                if full_map[coord4_h[1]][coord4_h[0]]==full_map[coord4[1]][coord4[0]]:
                    if full_map[coord5_h[1]][coord5_h[0]]==full_map[coord5[1]][coord5[0]]:
                        if full_map[coord6_h[1]][coord6_h[0]]==full_map[coord6[1]][coord6[0]]:
                            if full_map[coord7_h[1]][coord7_h[0]]==full_map[coord7[1]][coord7[0]]:
                                if full_map[coord8_h[1]][coord8_h[0]]==full_map[coord8[1]][coord8[0]]:
                                    if full_map[coord9_h[1]][coord9_h[0]]==full_map[coord9[1]][coord9[0]]:
                                        if full_map[coord10_h[1]][coord10_h[0]]==full_map[coord10[1]][coord10[0]]:
                                            return True
    return False

def chebychev_distance(x1,x2,y1,y2):
    y_dist = abs(y1 - y2)
    x_dist = abs(x1- x2)
    return max(x_dist,y_dist)

def astar_crusader(vis,loc,pass_map,goal,cost):
    vbot = []
    for bot in vis:
        vbot.append(bot['x'],bot['y'])

    q = util.PriorityQueue()
    q.push((loc[0],loc[1],0),0)

    size = len(pass_map)

    # False means visited or impassable here
    visited = []
    wave = []
    for i in range(len(pass_map)):
        row = []
        wrow = []
        for k in range(len(pass_map)):
            wrow.append(1000)
            if pass_map[i][k] == False:
                row.append(1)
            else:
                row.append(0)
        visited.append(row)

    j = -1

    while q.isEmpty() == False and j <= 50:
        j += 1
        (cx,cy,cs) = q.pop()

        if not visited[cy][cx]:
            visited[cy][cx] = 2

            wave[cy][cx] = cs

            for xi in range(-3,4):
                for yi in range(-3,4):
                    if xi**2 + yi**2 < 9:
                        newx = cx + xi
                        newy = cy + yi

                        if (newx > size-1 or newy > size-1 or 0 > newy or 0 > newx):
                            continue
                            
                        if visited[newy][newx] == 1:
                            continue

                        if int(util.nodeHash(newx,newy)) in vbot:
                            continue 

                        f = 1 + chebychev_distance(newx,goal[0],newy,goal[1]) + cs #+ (xi**2 + yi**2)*cost
                        q.push((newx,newy,f),f)

    score = 1e32
    action = (0,0)
    for xi in range(-3,4):
        for yi in range(-3,4):
            if xi**2 + yi**2 < 9:
                newx = loc[0] + xi
                newy = loc[1] + yi

                if visited[newy][newx] == 1 or newx > size-1 or newy > size-1 or 0 > newy or 0 > newx:
                    continue;

                if x[newx][newy] < score:
                    score = x[newx][newy]
                    action = (xi,yi)

    return action









