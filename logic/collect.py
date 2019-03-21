import var
from logic import algo
from motion import smart


def box_collection(robot):
    '''
    Collect all boxes
    :return: None
    '''

    #    Collecting unknown box
    if var.unknown_boxes > 0:
        robot.status = 'traverse'
        route = algo.field_traverse(robot.coords, var.was_not, var.base_field)
        robot.route = algo.straight_routes(route)
        smart.move(robot)

    #    Collecting known boxes
    while var.box_coords:
        robot.status = 'collect'
        min_route = []
        for box in var.box_coords:
            route = algo.get_route(robot.coord, box, var.base_field)
            if (len(route) < len(min_route) or not min_route) and (box not in robot.another_robot.route[-1])\
                    or not robot.another_robot.localized:
                min_route = route

        if not min_route:  # another robot drive to the last box, we need drive to reset_point
            break

        # Moving on min_route
        robot.route = algo.straight_routes(min_route)
        smart.move(robot)


