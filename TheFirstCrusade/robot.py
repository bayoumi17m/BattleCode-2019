from battlecode import BCAbstractRobot, SPECS
import battlecode as bc
import random
import nav
import util
# import time
# import copy

__pragma__('iconv')
__pragma__('tconv')
__pragma__('opov')



# don't try to use global variables!!
class MyRobot(BCAbstractRobot):

    karboniteMining = True

    wave = []
    homePath = (0,0)
    visited = []
    mapSize = 0

    already_been = {}
    base = None
    destination = None

    def turn(self):
        if self.me['unit'] == SPECS['CRUSADER']:
            self.log("Crusader health: " + str(self.me['health']))

            visible = self.get_visible_robots()

            # get attackable robots
            attackable = []
            for r in visible:
                # x = 5
                if not self.is_visible(r):
                    # this robot isn't actually in our vision range, it just turned up because we heard its radio broadcast. disregard.
                    continue
                # now all in vision range, can see x, y etc
                dist = (r['x'] - self.me['x'])**2 + (r['y'] - self.me['y'])**2
                if r['team'] != self.me['team'] and SPECS['UNITS'][SPECS["CRUSADER"]]['ATTACK_RADIUS'][0] <= dist <= SPECS['UNITS'][SPECS["CRUSADER"]]['ATTACK_RADIUS'][1]:
                    attackable.append(r)

            if attackable:
                # attack first robot
                r = attackable[0]
                self.log('attacking! ' + str(r) + ' at loc ' + (r['x'] - self.me['x'], r['y'] - self.me['y']))
                return self.attack(r['x'] - self.me['x'], r['y'] - self.me['y'])


            
            # # The directions: North, NorthEast, East, SouthEast, South, SouthWest, West, NorthWest
            my_coord = (self.me['x'], self.me['y'])
            self.already_been[my_coord] = True
            # self.log(nav.symmetric(self.map)) #for some reason this would sometimes throw an error
            # self.log("My destination is "+self.destination)
            if not self.destination:
                self.log("trying to move")
                self.destination = nav.reflect(self.map, my_coord, nav.symmetric(self.map))
            self.log("Trying to move to "+ self.destination)

            # goal_dir=nav.goto(my_coord, self.destination, self.map, self.get_visible_robot_map(), self.already_been)
            # x=0
            # jump_dir=goal_dir
            # while x<2:
            #     loc=nav.apply_dir(my_coord,jump_dir)
            #     self.already_been[loc] = True
            #     goal_dir=nav.goto(loc, self.destination, self.map, self.get_visible_robot_map(), self.already_been)
            #     x=x+1
            #     jump_dir=jump_dir[0]+goal_dir[0],jump_dir[1]+goal_dir[1]

            # if jump_dir[0]**2+jump_dir[1]**2>9:
            #     self.log("not sure")
            #     jump_dir=jump_dir[0]-goal_dir[0],jump_dir[1]-goal_dir[1]
            #     if nav.symmetric(self.map):
            #         jump_dirh=jump_dirh[0],jump_dir[1]+1
            #         loc=nav.apply_dir(my_coord,jump_dir)
            #         self.log("hi")
            #         if jump_dirh[0]**2+jump_dirh[1]**2<9 and nav.is_passable(self.map,loc,jump_dirh,self.get_visible_robot_map()):
            #             return self.move(*jump_dirh[0],jump_dir[1]+1)
            #         else:
            #             return self.move(*jump_dir)
            #     else:
            #         jump_dirv=jump_dir[0]+1,jump_dir[1]
            #         loc=nav.apply_dir(my_coord,jump_dir)
            #         self.log("bye")
            #         if jump_dirv[0]**2+jump_dirv[1]**2<9 and nav.is_passable(self.map,loc,jump_dirv,self.get_visible_robot_map()):
            #             return self.move(*jump_dirv)
            #         else:
            #             return self.move(*jump_dir)

            # self.log("why")
            # loc=nav.apply_dir(my_coord,jump_dir)
            # self.log("this should not even be returning "+loc)
            # return self.move(*jump_dir)
            goal_dir=nav.goto(my_coord, self.destination, self.map, self.get_visible_robot_map(), self.already_been)
            #return self.move(*nav.goto(my_coord, self.destination, self.map, self.get_visible_robot_map(), self.already_been))
            self.log(goal_dir)
            return self.move(*goal_dir)
               
        elif self.me['unit'] == SPECS['CASTLE']:
            # self.log("the map is "+ nav.symmetric(self.map))
            my_coord = (self.me['x'], self.me['y'])
            if self.me['turn']<2:
                goal_dir=nav.spawn(my_coord, self.map, self.get_visible_robot_map())
                self.log(self.me['turn'])
                self.log("Building a Prophet at " + str(self.me['x']+goal_dir[0]) + ", " + str(self.me['y']+goal_dir[1]))
                return self.build_unit(SPECS['PROPHET'], goal_dir[0],goal_dir[1])

            if self.me['turn'] < 4:
                if not self.karboniteMining:
                    mapEnergy = self.get_fuel_map()
                    self.karboniteMining  = True
                else:
                    mapEnergy = self.get_karbonite_map()
                    self.karboniteMining = False

                # size = len(mapEnergy) -1
                # dist = 121
                # targetX = "0"
                # targetY = "0"
                # for i in range(-20,21):
                #     for k in range(-20,21):
                #         if self.me['y'] + i < 0 or self.me['x'] + k < 0 or self.me['y'] + i > size or self.me['x'] + k > size:
                #             continue
                #         if mapEnergy[self.me['y'] + i][self.me['x'] + k] and i**2 + k**2 < dist:
                #             targetX = str(self.me['x'] + k)
                #             targetY = str(self.me['y'] + i)
                #             dist = i**2 + k**2
                targetX, targetY = nav.get_closest_karbonite((self.me['x'],self.me['y']), mapEnergy)
                targetX = str(targetX); targetY = str(targetY)

                self.signal(int("" + str(len(targetX)) + targetX + targetY),2)

                self.log("Building a Pilgrim at " + str(self.me['x']+1) + ", " + str(self.me['y']+1))
                goal_dir=nav.spawn(my_coord, self.map, self.get_visible_robot_map())
                return self.build_unit(SPECS['PILGRIM'], goal_dir[0], goal_dir[1])
            elif self.me['turn'] < 50:
                goal_dir=nav.spawn(my_coord, self.map, self.get_visible_robot_map())
                self.log("Building a crusader at " + str(self.me['x']+goal_dir[0]) + ", " + str(self.me['y']+goal_dir[1]))
                return self.build_unit(SPECS['CRUSADER'], goal_dir[0],goal_dir[1])
            else:
                pass
                # self.log("Castle health: " + self.me['health'])
        
        elif self.me['unit'] == SPECS['PILGRIM']:
            if self.me['turn'] == 1:
                # Map Building
                # fuelMap = self.fuel_map
                self.homePath = (self.me['x'],self.me['y'])

                # passMap = self.map
                # # karbMap = self.karbonite_map
                # self.mapSize = len(passMap)
                # for y in range(self.mapSize):
                #     row = []
                #     vrow = []
                #     for x in range(self.mapSize):
                #         vrow.append(0)
                #         if passMap[y][x] == False:
                #             row.append(0)
                #         else:
                #             row.append(0)
                #     self.wave.append(row)
                #     self.visited.append(vrow)


                # Read Signal!
                signal = ""
                for botv in self.get_visible_robots():
                    if self.is_radioing(botv) and botv['unit'] == SPECS["CASTLE"]:
                        signal = str(botv['signal'])
                        break

                parsePoint = int(signal[0])
                y = int(signal[parsePoint+1:])
                x = int(signal[1:parsePoint+1])
                # self.log("Signal is: " + signal + " and target is: " + str((x,y)))

                # self.wave[y][x] = 2
                self.targetX = x
                self.targetY = y
                # self.log("The target is: " + str((self.targetX,self.targetY)))

                moves = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
                path = nav.astar(self.log, self.get_visible_robots(), self.get_passable_map(), (self.me['x'],self.me['y']), (self.targetX,self.targetY), moves)
                # for node in path:
                #     self.log("Path " + str((node.x,node.y)))
                action = (path[1].x - self.me['x'], path[1].y - self.me['y'])
                # self.log("Trying to move by: " + str(action) + " from " + str((self.me['x'],self.me['y'])))
                return self.move(*action)

            if self.me['turn'] > 1:

                karbMiner = self.get_karbonite_map()[self.targetY][self.targetX]
                # self.log("karbMiner: " + str(karbMiner))

                if karbMiner:
                    energy = 'karbonite'
                    capacity = SPECS['UNITS'][SPECS['PILGRIM']]['KARBONITE_CAPACITY']
                else:
                    energy = 'fuel'
                    capacity = SPECS['UNITS'][SPECS['PILGRIM']]['FUEL_CAPACITY']

                # botv_pos = []
                # for botv in self.get_visible_robots():
                #     botv_pos.append(util.nodeHash(botv.x,botv.y))
                    
                if util.nodeHash(self.me['x'],self.me['y']) == util.nodeHash(self.targetX,self.targetY) and self.me[energy] < capacity:
                    # self.log("MINING")
                    # self.log(energy + " " + str(self.me[energy]) + "/" + str(capacity))
                    return self.mine()

                elif self.me[energy] < capacity and util.nodeHash(self.me['x'],self.me['y']) != util.nodeHash(self.targetX,self.targetY):
                    # self.log("Moving!!!")
                    moves = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
                    path = nav.astar(self.log, self.get_visible_robots(), self.get_passable_map(), (self.me['x'],self.me['y']), (self.targetX,self.targetY), moves)
                    action = (path[1].x - self.me['x'], path[1].y - self.me['y'])
                    return self.move(*action)

                elif self.me[energy] == capacity and util.nodeHash(*self.homePath) != util.nodeHash(self.me['x'],self.me['y']):
                    # self.log("WORKING LOOP")
                    moves = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]

                    path = nav.astar(self.log,self.get_visible_robots(), self.get_passable_map(), (self.me['x'],self.me['y']), self.homePath, moves)
                    action = (path[1].x - self.me['x'], path[1].y - self.me['y'])
                    return self.move(*action)


                else:
                    for botv in self.get_visible_robots():
                        if botv['unit'] == SPECS['CASTLE'] or botv['unit'] == SPECS['CHURCH']:
                            break;
                    # self.log(str(self.me['karbonite']))
                    return self.give(botv['x'] - self.me['x'],botv['y'] - self.me['y'], self.me['karbonite'], self.me['fuel'])

robot = MyRobot()