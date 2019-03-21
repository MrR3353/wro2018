import var
from logic import algo
from motion import smart


def escape(robot):
    '''
    Drop boxes and escape to the last coord
    Running only if both robot localized
    '''

    def to_1dim(ls):
        '''
        Converts 2dim to 1dim
        '''
        res = []
        for i in ls:
            res += i
        return res

    if robot.col_box_coords:    # need to drop boxes
        # move to resetpoint
        route = algo.get_route(robot.coord, var.reset_point, var.base_field)
        robot = algo.straight_routes(route)
        smart.move(robot)

        if robot.another_robot.status == 'escape' and robot.another_robot.col_box_coords or robot.another_robot.status == 'end':
            # drop at center
            route = algo.get_route(robot.reset_point, robot.another_robot.start_coord, var.base_field)
            smart.throw_boxes(robot, route[1])
        else:
            # another robot don't dropped anything
            route_another = to_1dim(robot.another_robot.route)
            if robot.another_robot.col_box_coords or var.reset_point in route_another:
                #  transfer boxes to another
                prev = ()  # coord another before reset_point
                if route_another[-1] == var.reset_point:
                    prev = route_another[-2]
                else:   # another drive to the last box
                    prev = algo.get_route(var.box_coords[0], var.reset_point, var.base_field)[-2]

                #   drop for another robot
                route = algo.get_route(robot.reset_point, robot.another_robot.start_coord, var.base_field)
                smart.throw_boxes(robot, route[1], prev)
            else:
                #   drop boxes at center
                route = algo.get_route(robot.reset_point, robot.another_robot.start_coord, var.base_field)
                smart.throw_boxes(robot, route[1])

    # escape
    route = algo.get_route(robot.coord, robot.another_robot.start_coord, var.base_field)
    robot.route = algo.straight_routes(route)
    robot.status = 'escape'
    smart.move(robot)

    robot.status = 'end'




