import math
import time

import var
from logic.algo import shift_cell


def forward(robot, n):
    '''
    move - passage of n cells
    
    :Param robot - link to object robot
    :Param n - number of cells
    '''

    if var.classic:
        robot.link_move.move(n)

    for _ in range(n):
        x = round(robot.coord[0] + math.sin(robot.alpha*math.pi/180))
        y = round(robot.coord[1] + math.cos(robot.alpha*math.pi/180))
        x_real = round(robot.real_coord[0] + math.sin(robot.real_alpha*math.pi/180))
        y_real = round(robot.real_coord[1] + math.cos(robot.real_alpha*math.pi/180))
        robot.coord = (x,y)
        robot.real_coord = (x_real, y_real)
        if var.visual and not var.classic:
            time.sleep(0.8)


def rotate(robot, alpha):
    '''
    rotate - turn on to alpha
    
    :Param robot - link to object robot
    :Param alpha - alpha
    '''

    ang = alpha - robot.alpha
    if ang == 270:
        ang = -90
    elif ang == -270:
        ang = 90
    robot.alpha = alpha
    # robot.real_alpha = (robot.real_alpha + ang)%360
    
    if var.classic:
        robot.link_move.rotate(ang)
    if var.visual and not var.classic:
        time.sleep(0.8)


def collect(robot):
    '''
    collect - Change the rotation mode of the grasping wheels on the gripper

    Param robot - link to object robot
    '''

    if var.classic:
        robot.link_move.collect()


def deploy(robot, center=True):
    '''
    Drop boxes
    :param in_middle: do we drop boxes in the center with back moving
    '''

    def back(robot, dist):
        '''
        back - back movement to dist

        :Param robot - link to object robot
        :Param dist - distance
        '''

        if var.classic:
            robot.link_move.back(dist)

    if center:
        back(robot, dist=0)  # move back for throwing

        if var.classic:
            robot.link_move.deploy()

        # TODO: Here mustn't stay another robot
        # move back to next coord.
        back(robot, dist=50)

        # change robot.coord
        if robot.alpha == 0:
            robot.coord = (robot.coord[0] - 1, robot.coord[1])
        elif robot.alpha == 180:
            robot.coord = (robot.coord[0] + 1, robot.coord[1])
        elif robot.alpha == 90:
            robot.coord = (robot.coord[0], robot.coord[1] - 1)
        elif robot.alpha == 270:
            robot.coord = (robot.coord[0], robot.coord[1] + 1)
    else:
        if var.classic:
            robot.link_move.deploy()


def get_cell_data(robot):
    '''
    get_cell_data - Getting the type of cell

    :Param robot - link to object robot
    [1, 0, 0, 1]
    '''

    if var.classic:
        cell = robot.link_move.get_cell()
    elif var.visual:
        cell = var.field[robot.real_coord]
        cell = shift_cell(cell, robot.real_alpha)
    return cell



