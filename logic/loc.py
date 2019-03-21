from logic import algo
import copy
import var
from motion import smart

'''
Localization can't be done if our field is symmetric. Then we can consider 
positions of known boxes, but if this boxes stay also symmetric then we
never localize and have one of 2 variants layout 
'''


def check_coincidence(field_robot, field):
    '''
    check_coincidence - get number of matches

    :Param field_robot - Robot field
    :Param field       - field
    '''

    N = 0
    past_coords = list(field_robot.keys())
    first_coord_val = field_robot[0, 0]
    past_coords.remove((0, 0))
    for coord, val in field.items():
        if val == first_coord_val:
            n = 0
            for past_coord in past_coords:
                x = coord[0] + past_coord[0]
                y = coord[1] + past_coord[1]
                if (x, y) in field:
                    if field_robot[past_coord] == field[x, y]:
                        n += 1
                    else:
                        break
                else:
                    break
            if n == len(past_coords):
                N += 1
    return N


def get_coord(field_robot, field, coord_robot):
    '''
    get_coord - obtaining a robot coordinate

    :Param field_robot - Robot field
    :Param field       - field
    :Param coord_robot - coordinate
    '''

    past_coords = list(field_robot.keys())
    first_coord_val = field_robot[0, 0]
    past_coords.remove((0, 0))
    for coord, val in field.items():
        if val == first_coord_val:
            n = 0
            for past_coord in past_coords:
                x = coord[0] + past_coord[0]
                y = coord[1] + past_coord[1]
                if (x, y) in field:
                    if field_robot[past_coord] == field[x, y]:
                        n += 1
                    else:
                        break
                else:
                    break
            if n == len(past_coords):
                x = coord[0] + coord_robot[0]
                y = coord[1] + coord_robot[1]
                break
    return y, x


def localization(robot):
    '''
    Localization process.
    :return:
    '''

    # TODO: if var.met and robot localized, we must at once localize another robot

    smart.first_scan(robot)

    matches = 0
    real_angle = 0
    while matches != 1 or not robot.localized:

        # check matches
        matches = 0
        for angle in (0, 90, 180, 270):
            matches += check_coincidence(robot.field, var.field[angle])
            if matches == 1:
                real_angle = angle
            if matches > 1:    # optimization
                break

        # moves to nearest unknown cell
        route = algo.route2unknown(robot.coord, robot.field)
        robot.route = algo.straight_routes(route)
        smart.move(robot)

    if robot.localized:
        # one of robots localized in past and now they met.
        # localization of this robot was in smart
        return

    absolute_coord = get_coord(robot.field, var.field[real_angle], robot.coord)

    if var.met and not robot.another_robot.localized:
        # localization another robot (robots met in past and now one of them localized)
        # TODO: test this code!!!
        coord_dif = robot.another_robot.coord[0] - robot.coord[0], robot.another_robot.coord[1] - robot.coord[1]
        alp_dif = robot.another_robot.alpha - robot.alpha
        absolute_coord2 = absolute_coord[0] + coord_dif[0], absolute_coord[1] + coord_dif[1]

        robot = robot.another_robot

        for coord in robot.col_box_coords:  # update to absolute coords
            robot.col_box_coords.remove(coord)
            robot.col_box_coords.append((coord[0] - robot.coord[0] + absolute_coord[0],
                                         coord[1] - robot.coord[1] + absolute_coord[1]))

        # Removing collected boxes from box_coords
        for coord in robot.col_box_coords:
            if coord in var.box_coords:
                var.box_coords.remove(coord)
            else:
                var.unknown_boxes -= 1

        robot.start_coord = (absolute_coord2[0] - robot.coord[0] + robot.start_coord[0],
                             absolute_coord2[1] - robot.coord[1] + robot.start_coord[1])
        robot.coord = absolute_coord2
        robot.alpha = (real_angle + robot.another_robot.alpha + alp_dif) % 360
        robot.localized = True

        robot = robot.another_robot

    # Clearing was_not (if var.met we don't do it again since robots have common field)
    for coord in robot.field:
        if (coord[0] - robot.coord[0] + absolute_coord[0], coord[1] - robot.coord[1] + absolute_coord[1]) in var.was_not:
            var.was_not.remove(coord)

    for coord in robot.col_box_coords:  # update to absolute coords
        robot.col_box_coords.remove(coord)
        robot.col_box_coords.append((coord[0] - robot.coord[0] + absolute_coord[0],
                                     coord[1] - robot.coord[1] + absolute_coord[1]))

    # Removing collected boxes from box_coords
    for coord in robot.col_box_coords:
        if coord in var.box_coords:
            var.box_coords.remove(coord)
        else:
            var.unknown_boxes -= 1

    robot.start_coord = (absolute_coord[0] - robot.coord[0] + robot.start_coord[0],
                         absolute_coord[1] - robot.coord[1] + robot.start_coord[1])
    robot.coord = absolute_coord
    robot.alpha = (real_angle + robot.alpha) % 360
    robot.localized = True

