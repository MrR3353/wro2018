import var
import time
from motion import simple
from logic import algo


def get_turn_angle(coord1, coord2):
    '''
    Returns angle for turn for move from coord1 to coord2
    '''
    diff = (coord2[0] - coord1[0], coord2[1] - coord1[1])
    if diff == (0, 1):
        return 0
    elif diff == (0, -1):
        return 180
    elif diff == (1, 0):
        return 90
    elif diff == (-1, 0):
        return 270


def move(robot):
    '''
    Moving on robot.route[0]
    :param robot: Object of robot, that moves
    :return: None
    '''

    def check_conflict(robot):
        '''
        Checks if there are have any conflicts between roboots in route[0]
        :return:
        '''
        for coord in robot.route[0]:
            if coord in robot.another_robot.route[0]:
                return coord
        return None

    def divide_route(route, confl):
        '''
        Divides route[0] on 2 lists - before conflict and after it
        :param route: robot.route. Returns [[], ...] if route[0] == confl
        '''
        route.insert(0, [])
        ind = route[1].index(confl)
        route[0] = route[1][:ind]
        route[1] = route[1][ind:]

    # correction of robot.route
    if robot.route[0][0] == robot.coord:  # robot.route[0][0] never must be a robot.coord
        robot.route[0].remove(robot.coord)

    if not robot.route[0]:  # removing empty straight routes
        robot.route.remove([])

    while robot.route:

        if robot.localized and robot.another_robot.localized or var.met:
            # synchronous moving, drive several cells

            # if robot don't localized they move on their own fields
            # if robots met, then one of them change his dynamic data(coord, alpha)
            # relative of another, they combine their fields and their fields comes a common object
            # If one of them localized after it, they both localized

            confl = check_conflict(robot)
            if confl is None:
                # turn (if he is)
                simple.rotate(robot, get_turn_angle(robot.coord, robot.route[0][0]))

                # moving on route
                is_box = simple.forward(robot, len(robot.route[0]))
                # TODO: write box checking in simple.forward
                if is_box:
                    robot.col_box_coords.append(robot.coord)
                    if robot.localized:
                        if robot.coord in var.box_coords:
                            var.box_coords.remove(robot.coord)
                        else:
                            var.unknown_boxes -= 1
                            if not var.unknown_boxes:
                                # remains to collect known boxes (if we traverse at first)
                                # stops moving and drive to known boxes (or to reset point)
                                if robot.status == 'traverse':
                                    robot.route = []
                                if robot.another_robot.status == 'traverse':
                                    robot.another_robot.route = []
                                return
                    for coord in robot.route[0]:  # delete passed coords
                        robot.route[0].remove(coord)
                        if robot.localized:
                            if coord in var.was_not:    # clear was_not
                                var.was_not.remove(coord)
                        if robot.coord == coord:
                            break
                else:
                    for coord in robot.route[0]:
                        if robot.localized:
                            if coord in var.was_not:  # clear was_not
                                var.was_not.remove(coord)
                    robot.route.remove(robot.route[0])  # delete passed route

            else:
                # Now we just wait, when another robot arrived, but we can give him command to get out
                divide_route(robot.route, confl)
                if robot.route[0]:  # first cell in route isn't conflict, moving before conflict
                    # we can invoke a move() or just fall through to external while condition
                    continue
                else:
                    robot.route.remove([])
                    while robot.route[0][0] in robot.another_robot.route[0] or robot.route[0][0] == robot.another_robot.coord:

                        if robot.another_robot.wait or robot.another_robot.status == 'end':
                            # another robot don't move. We must to invoke get_out()
                            pass
                            # TODO: write algorithm, in order to choose robot, which must get_out()
                            # we must do it optimal in time
                            # if both robots wait we can do that one of them will wait and another will move
                        else:
                            # wait another robot
                            robot.wait = True
                            time.sleep(0.5)
                    robot.wait = False

        else:
            # moving step by step (in sequence)

            if robot.name == var.who_moves:

                # Check for conflict with another robot
                data = simple.get_cell_data(robot)
                cell = algo.shift_cell([data[0], data[1], 0, data[2]], (360 - robot.alpha) % 360)
                # TODO: check condition it must compare objects, not links
                if cell != robot.field[robot.coord]:
                    # robot contact with another. robot must drive to nearest unknown
                    # cell with dist = 1, (or just drive to his prev coord), further
                    # another move in prev coord of robot

                    # in order to don't confuse
                    robot.route = []
                    robot.another_robot.route = []

                    # if one of robot localized he must be first!
                    if robot.another_robot.localized:
                        robot = robot.another_robot    # this code is sh1t but i too lazy to decide it otherwise
                        data = simple.get_cell_data(robot)
                        cell = algo.shift_cell([data[0], data[1], 0, data[2]], (360 - robot.alpha) % 360)

                    side = 0    # num of side, where stay another robot (relative from robot.field)
                    for i in range(len(cell)):
                        if side[i] != robot.field[robot.coord][i]:
                            side = i

                    another_coord = None   # relative
                    another_alpha = None   # after 1 turn of another it will contain right value

                    if i == 0:
                        another_coord = robot.coord[0] - 1, robot.coord[1]
                        another_alpha = 180
                    elif i == 2:
                        another_coord = robot.coord[0] + 1, robot.coord[1]
                        another_alpha = 0
                    elif i == 1:
                        another_coord = robot.coord[0], robot.coord[1] + 1
                        another_alpha = 270
                    elif i == 3:
                        another_coord = robot.coord[0], robot.coord[1] - 1
                        another_alpha = 90

                    # Choose cell in order to drive away there
                    prev_coord = None
                    if robot.alpha == 0:
                        prev_coord = robot.coord[0] + 1, robot.coord[1]
                    if robot.alpha == 180:
                        prev_coord = robot.coord[0] - 1, robot.coord[1]
                    if robot.alpha == 90:
                        prev_coord = robot.coord[0], robot.coord[1] - 1
                    if robot.alpha == 180:
                        prev_coord = robot.coord[0], robot.coord[1] + 1

                    for diff in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                        coord = robot.coord[0] + diff[0], robot.coord[1] + diff[1]
                        if coord not in robot.field and coord != another_coord:
                            prev_coord = robot.coord[0] + diff[0], robot.coord[1] + diff[1]

                    # Now 1st move in prev_coord

                    relative_coord = robot.coord   # remember 1st coord now

                    #  turn (if it is)
                    simple.rotate(robot, get_turn_angle(robot.coord, prev_coord))
                    # move forward
                    is_box = simple.forward(robot, 1)
                    if is_box:
                        if robot.localized:
                            if robot.coord in var.box_coords:
                                var.box_coords.remove(robot.coord)
                            else:
                                var.unknown_boxes -= 1
                        robot.col_box_coords.append(robot.coord)

                    # 2nd moves in previous coord of 1st
                    diff = robot.coord[0] - another_coord[0], robot.coord[1] - another_coord[1]
                    coord2move = robot.another_robot.coord[0] + diff[0], robot.another_robot.coord[1] + diff[1]

                    # turn (if it is)
                    simple.rotate(robot.another_robot, get_turn_angle(robot.another_robot.coord, coord2move))
                    # move forward
                    simple.forward(robot.another_robot, 1)  # there is no box, because 1st stood here

                    # Ok, all right. Now just write in 2nd relative values,
                    # and if 1st localized, end localization
                    old_coord = robot.another_robot.coord   # need for field concatenation
                    old_alpha = robot.another_robot.alpha
                    robot.another_robot.coord = relative_coord
                    robot.another_robot.alpha = another_alpha

                    # if no one of robots localized, concatenate their fields and continue loc
                    # change all values to actual
                    diff = (robot.another_robot.coord[0] - old_coord[0],
                            robot.another_robot.coord[1] - old_coord[1])
                    for coord in robot.another_robot.field:
                        coord_now = (diff[0] + coord[0], diff[1] + coord[1])
                        if coord_now not in robot.field:
                            cell = algo.shift_cell(robot.another_robot.field[coord],
                                                   (old_alpha - robot.another_robot.alpha) % 360)
                            robot.field[coord_now] = cell

                    # TODO: check that i give link, and field is common object now
                    robot.another_robot.field = robot.field
                    robot.another_robot.start_coord = diff

                    for coord in robot.another_robot.col_box_coords:
                        robot.another_robot.col_box_coords.remove(coord)
                        robot.another_robot.col_box_coords.append((diff[0] + coord[0],
                                                                   diff[1] + coord[1]))

                    if robot.localized:  # Localize another robot
                        # Removing collected boxes from box_coords
                        for coord in robot.another_robot.col_box_coords:
                            if coord in var.box_coords:
                                var.box_coords.remove(coord)
                            else:
                                var.unknown_boxes -= 1
                        # Clearing was_not
                        for coord in robot.another_robot.field:
                            if coord in var.was_not:
                                var.was_not.remove(coord)

                        robot.another_robot.localized = True

                    # return to loc (routes = [])
                    return

                #  turn (if it is)
                simple.rotate(robot, get_turn_angle(robot.coord, robot.route[0][0]))

                # moving on route
                is_box = simple.forward(robot, 1)
                if is_box:
                    if robot.localized:
                        if robot.coord in var.box_coords:
                            var.box_coords.remove(robot.coord)
                        else:
                            var.unknown_boxes -= 1
                    robot.col_box_coords.append(robot.coord)
                robot.route.remove(robot.route[0][0])

                # get cell info (Gets 3 values from robot and 2th - always 0 if it's not a 1st cell)
                data = simple.get_cell_data(robot)
                robot.field[robot.coord] = algo.shift_cell([data[0], data[1], 0, data[2]], (360 - robot.alpha) % 360)

                var.who_moves = robot.another_robot.name


def first_scan(robot):
    data = simple.get_cell_data()
    simple.rotate(robot, 90)
    data2 = simple.get_cell_data()
    data.insert(2, data2[1])
    robot.field[robot.coord] = data

    # TODO: meeting with another robot

    # one of the walls is robot
    if data == [1, 1, 1, 1]:
        var.who_moves = robot.another_robot.name

    # do first move
    else:
        ind = 0
        for i in range(len(data)):
            if data[i] == 0:
                ind = i
        route = algo.route2unknown(robot.coord, robot.field)
        simple.rotate(robot, get_turn_angle(robot.coord, route[-1]))
        is_box = simple.forward(robot, 1)
        if is_box:
            robot.col_box_coords.append(robot.coord)


def get_out(robot):
    '''
    This method invokes when one robot blocks another.
    He must get out from another way
    Must invoke as get_out(robot.another_robot)
    :return:
    '''

    # TODO: We must be sure that another robot wait, while this robot get out
    # TODO: Robot must return to his coord after get_out()

    def in_another_route(coord):
        '''
        checks that coord contains in another route
        :return:
        '''
        for line in robot.another_robot.route:
            if coord in line:
                return True
        return False

    def copy_2dim_list(a):
        b = []
        for i in a:
            b.append(list(i))
        return b

    #  TODO: Maybe resetpoint will need to remove from for loop. (We can touch boxes inside this cell)
    min_route = []
    for coord in var.available_cells:
        if in_another_route(coord):
            continue
        # TODO: now we build bypass route, consider only dist to given cell. Need to try build route,
        # that don't conflict with current another robot coord
        route = algo.get_route(robot.coord, coord, var.base_field)
        if route < min_route or not min_route:
            min_route = route

    # if robot don't ended we need to store his own route then he get_out()
    old_route = copy_2dim_list(robot.route)
    robot.route = algo.straight_routes(min_route)

    # moving on min_route
    move(robot)

    # wait until another drives previous self coord
    while robot.another_robot.coord != min_route[-2]:
        time.sleep(0.5)

    # TODO: robot must return only in needed cells (Create separate variable or smt another where we can
    # cells that we need to visit(Not routes to they))
    # get back
    min_route.reverse()
    route = algo.straight_routes(min_route)
    robot.route = route + old_route
    move(robot)


def throw_boxes(robot, next_coord, another_r_coord=None):
    '''
    Smart throwing, we consider moving in the next coord

    :param next_coord:
    :param another_r_coord: coord in which another robot will stay before coming to reset_point
    '''
    if another_r_coord is None:
        angle = get_turn_angle(robot.coord, (next_coord+180) % 360)
        simple.rotate(robot, angle)
        simple.deploy(robot)
    else:
        angle = get_turn_angle(robot.coord, another_r_coord)
        simple.rotate(robot, angle)
        simple.deploy(robot, center=False)
        angle = get_turn_angle(robot.coord, next_coord)
        simple.rotate(robot, angle)



