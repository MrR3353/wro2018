import rpyc

import logic
import var
import time
from motion import smart

'''
robot.py - file that describes robot class.
Includes:
1. Localization 
2. Moves to known boxes
3. Moves to unknown box
4. Moves to boxes cell
5. Moves to another robot start
'''

'''
TODO: If one robot can't build a route(2nd stay at his way) we must give a command to 2nd, that he must drive
in coord that don't contains in route of 1st robot.
Need function to check if route, that was build is correct
'''


class Robot:

    name = ''  # name of robot. (Eva/Rob)
    another_robot = None  # Link to another robot
    link_move = None  # Link to module move

    localized = False   # Is the robot localized?
    wait = False    # waiting another robot
    status = ''     # traverse/collect/drop/escape/end or sth else

    # Variables below can be relative/absolute
    field = {(0,0):[0,1,1,1], (0,1):[0,1,0,1], (0,2):[1,0,0,1], (1,2):[1,0,1,0], (2,2):[1,0,1,0], (3,2):[1,0,1,0], (4,2):[1,1,0,0], (4,1):[0,1,0,1], (4,0):[0,1,1,1]}      # Robot field
    coord = (0, 0)  # Robot coord. Can be changed only in simple/moves
    alpha = 0   # Robot direction. Can be changed only in simple/moves
    col_box_coords = [(5, 3)]  # coords of collected boxes (for statistics and loc)
    route = []  # list of straight routes. [[], [], ...]
    start_coord = (0, 0)

    def __init__(self, ip=None):
        if var.classic:
            self.rbt = rpyc.classic.connect(ip)
            self.link_move = self.rbt.modules["move"]

    def run(self):
        logic.loc.localization(self)
        logic.collect.box_collection(self)
        while not self.another_robot.localized:
            time.sleep(1000)
            # help another to localize
        logic.final.escape(self)

