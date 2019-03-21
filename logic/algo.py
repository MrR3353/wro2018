import copy
import time
import var

def shift_cell(cell, ang):
    '''
    shift_cell - rotation of the cell by the angle ang  

    :Param cell - rotatable cell
    :Param ang - rotation angle 
    '''

    for _ in range(ang//90):
        cell = cell[-1:] + cell[:-1]
    return cell


def shift_field(field, ang):
    '''
    shift_field - turn on the field

    :Param field - field
    :Param ang   - rotation angle
    '''

    # TODO: do it for non-rectangle field
    ret_field = {}
    for coord, cell in field.items():
        cell = copy.deepcopy(cell)
        x = coord[0]
        y = coord[1]
        for _ in range(int(ang / 90)):
            cell.insert(0, cell.pop(3))
            tmp = x
            x = y
            y = 7 - tmp
        ret_field[x, y] = cell
    return ret_field


def get_graph(field):
    '''
    Build a graph for dkstr algorithm
    :param field:
    :return:
    '''
    field_graph = {}
    for coord, val in field.items():
        template = []
        field_graph[coord] = template
        for i in range(4):
            if val[i] == 0:
                if i == 0:
                    x = coord[0]
                    y = coord[1] + 1
                elif i == 1:
                    x = coord[0] + 1
                    y = coord[1]
                elif i == 2:
                    x = coord[0]
                    y = coord[1] - 1
                elif i == 3:
                    x = coord[0] - 1
                    y = coord[1]
                field_graph[coord].append((x, y))
    return field_graph


def get_route(beg, end, field):
    '''
    Dejkstra algorithm.
    :param beg: start position
    :param end: end position
    :param field:
    :return: Route from beg to end
    '''


    field_graph = get_graph(field)
    field_routes = {}
    field_routes[beg] = [beg]
    branches = [beg]
    depth = 1
    while True:
        for coord in branches:
            for near_coord in field_graph[coord]:
                if near_coord not in field_routes:
                    field_routes[near_coord] = field_routes[coord] + [near_coord]
        tmp = branches
        branches = []
        for coord in tmp:
            for cord in field_graph[coord]:
                if len(field_routes[cord]) == depth + 1:
                    branches += [cord]

        if end in field_routes:
            return field_routes[end]
        if not branches:
            return None
        depth += 1


def get_all_routes(beg, field):
    '''
    Dejkstra algorithm.
    :param beg: start position
    :param end: end position
    :param field:
    :return: Routes to from beg to all available cells
    '''


    field_graph = get_graph(field)
    field_routes = {}
    field_routes[beg] = [beg]
    branches = [beg]
    depth = 1
    while True:
        for coord in branches:
            for near_coord in field_graph[coord]:
                if near_coord not in field_routes:
                    field_routes[near_coord] = field_routes[coord] + [near_coord]
        tmp = branches
        branches = []
        for coord in tmp:
            for cord in field_graph[coord]:
                if len(field_routes[cord]) == depth + 1:
                    branches += [cord]

        if not branches:
            return field_routes
        depth += 1


def route2unknown(beg, field_robot):
    '''
    route2unknown - return route to the nearest unknown coordinate

    :Param beg         - start position
    :Param field_robot - Robot field / field of known coordinates
    TODO: it is breaks when all field known
    '''

    field_graph = get_graph(field_robot)
    field_routes = {}
    field_routes[beg] = [beg]
    branches = [beg]
    depth = 1
    while True:
        for coord in branches:
            for near_coord in field_graph[coord]:
                if near_coord not in field_routes:
                    return field_routes[coord] + [near_coord]
                if near_coord not in field_routes:
                    field_routes[near_coord] = field_routes[coord] + [near_coord]
        tmp = branches
        branches = []
        for coord in tmp:
            for cord in field_graph[coord]:
                if len(field_routes[cord]) == depth + 1:
                    branches += [cord]

        depth += 1


def field_traverse(start, coords, field):
    '''
    Modified nearest neighbour algorithm
    :param start: start point
    :param coords: coordinates, that we must visit (var.was_not)
    :param field: var.base_field
    :return:
    '''

    def list_copy(x):
        '''
        Return copy list of dict
        :param x:
        :return:
        '''
        y = []
        for i in x:
            y.append(i)
        return y

    def build_graph(coords, field):
        '''
        Gets distances for all coords on field
        Need to rewrite for optimization
        :param coords:
        :param field:
        :return:
        '''
        all_dist = {}
        for i in range(len(coords)):
            tmp = {}
            routes = get_all_routes(coords[i], field)
            for j in routes:
                tmp[j] = routes[j]
            all_dist[coords[i]] = tmp
        return all_dist

    graph = build_graph(coords, field)
    dist = {}
    for coord in graph:
        tmp = {}
        for j in graph[coord]:
            tmp[j] = len(graph[coord][j]) - 1
        dist[coord] = tmp

    def real_route(route):
        '''
        Returns real route on given coords
        :param route:
        :return:
        '''
        res = []
        for i in range(len(route) - 1):
            res += graph[route[i]][route[i+1]][0:-1]
        return res

    route = {}

    k = 0
    route[k] = []
    coords_cur = list_copy(coords)
    current = start  # current position
    while coords_cur:
        # until we don't achieve all cell do
        minlen = dist[current][coords_cur[0]]
        minind = 0
        for i in range(1, len(coords_cur)):
            if dist[current][coords_cur[i]] < minlen:
                minlen = dist[current][coords_cur[i]]
                minind = i
        current = coords_cur[minind]
        route[k].append(current)
        coords_cur.remove(current)
    route[k] = real_route(route[k])
    # print(len(route[k]))

    k = 1
    route[k] = []
    coords_cur = list_copy(coords)
    current = start
    while coords_cur:
        # until we don't achieve all cell do
        minlen = dist[current][coords_cur[0]]
        minind = 0
        for i in range(1, len(coords_cur)):
            if dist[current][coords_cur[i]] < minlen:
                minlen = dist[current][coords_cur[i]]
                minind = i
            # if it equal we need to choose cell in deadblock or with more further ways to all cells
            # TEST: need to test code below (if condition) it can do route shorter or longer
            if dist[current][coords_cur[i]] == minlen:
                near_i = sum(
                    [(1 if dist[coords_cur[i]][j] == 1 else 0) for j in dist[coords_cur[i]]])  # count of adjacent cells for 1st
                near_min = sum([(1 if dist[coords_cur[minind]][j] == 1 else 0) for j in dist[coords_cur[minind]]])  # for 2nd
                if near_i < near_min:
                    minind = i
                # Addition modification. We visit furthest cell
                elif near_i == near_min:
                    if sum([dist[coords_cur[i]][j] for j in dist[coords_cur[i]]]) > sum(
                            [dist[coords_cur[minind]][j] for j in dist[coords_cur[minind]]]):
                        minind = i
        current = coords_cur[minind]
        route[k].append(current)
        coords_cur.remove(current)
    route[k] = real_route(route[k])
    # print(len(route[k]))

    k = 2
    route[k] = []
    coords_cur = list_copy(coords)
    current = start
    while coords_cur:
        # until we don't achieve all cell do
        minlen = dist[current][coords_cur[0]]
        minind = 0
        for i in range(1, len(coords_cur)):
            if dist[current][coords_cur[i]] < minlen:
                minlen = dist[current][coords_cur[i]]
                minind = i
            # if it equal we need to choose cell in deadblock or with more further ways to all cells
            # TEST: need to test code below (if condition) it can do route shorter or longer
            if dist[current][coords_cur[i]] == minlen:
                near_i = sum(
                    [(1 if dist[coords_cur[i]][j] == 1 else 0) for j in dist[coords_cur[i]]])  # count of adjacent cells for 1st
                near_min = sum([(1 if dist[coords_cur[minind]][j] == 1 else 0) for j in dist[coords_cur[minind]]])  # for 2nd
                if near_i < near_min:
                    minind = i
                # Addition modification. We visit furthest cell
                elif near_i == near_min:
                    if sum([dist[coords_cur[i]][j] for j in dist[coords_cur[i]]]) < sum(
                            [dist[coords_cur[minind]][j] for j in dist[coords_cur[minind]]]):
                        minind = i
        current = coords_cur[minind]
        route[k].append(current)
        coords_cur.remove(current)
    route[k] = real_route(route[k])
    # print(len(route[k]))

    k = 3
    route[k] = []
    coords_cur = list_copy(coords)
    current = start
    while coords_cur:
        # until we don't achieve all cell do
        minlen = dist[current][coords_cur[0]]
        minind = 0
        for i in range(1, len(coords_cur)):
            if dist[current][coords_cur[i]] < minlen:
                minlen = dist[current][coords_cur[i]]
                minind = i
            # if it equal we need to choose cell in deadblock or with more further ways to all cells
            # TEST: need to test code below (if condition) it can do route shorter or longer
            if dist[current][coords_cur[i]] == minlen:
                near_i = sum(
                    [(1 if dist[coords_cur[i]][j] == 1 else 0) for j in dist[coords_cur[i]]])  # count of adjacent cells for 1st
                near_min = sum([(1 if dist[coords_cur[minind]][j] == 1 else 0) for j in dist[coords_cur[minind]]])  # for 2nd
                if near_i > near_min:
                    minind = i
                # Addition modification. We visit furthest cell
                elif near_i == near_min:
                    if sum([dist[coords_cur[i]][j] for j in dist[coords_cur[i]]]) > sum(
                            [dist[coords_cur[minind]][j] for j in dist[coords_cur[minind]]]):
                        minind = i
        current = coords_cur[minind]
        route[k].append(current)
        coords_cur.remove(current)
    route[k] = real_route(route[k])
    # print(len(route[k]))

    k = 4
    route[k] = []
    coords_cur = list_copy(coords)
    current = start
    while coords_cur:
        # until we don't achieve all cell do
        minlen = dist[current][coords_cur[0]]
        minind = 0
        for i in range(1, len(coords_cur)):
            if dist[current][coords_cur[i]] < minlen:
                minlen = dist[current][coords_cur[i]]
                minind = i
            # if it equal we need to choose cell in deadblock or with more further ways to all cells
            # TEST: need to test code below (if condition) it can do route shorter or longer
            if dist[current][coords_cur[i]] == minlen:
                near_i = sum(
                    [(1 if dist[coords_cur[i]][j] == 1 else 0) for j in dist[coords_cur[i]]])  # count of adjacent cells for 1st
                near_min = sum([(1 if dist[coords_cur[minind]][j] == 1 else 0) for j in dist[coords_cur[minind]]])  # for 2nd
                if near_i > near_min:
                    minind = i
                # Addition modification. We visit furthest cell
                elif near_i == near_min:
                    if sum([dist[coords_cur[i]][j] for j in dist[coords_cur[i]]]) < sum(
                            [dist[coords_cur[minind]][j] for j in dist[coords_cur[minind]]]):
                        minind = i
        current = coords_cur[minind]
        route[k].append(current)
        coords_cur.remove(current)
    route[k] = real_route(route[k])
    # print(len(route[k]))

    route_min = route[0]
    for i in range(1, k):
        if len(route[i]) < len(route_min):
            route_min = route[i]

    return route_min


def straight_routes(route):
    '''
    Builds a list of straight routes from route
    :param route:
    :return: list of list of coords
    '''

    if len(route) == 1:
        return [route]

    def get_axis(coord1, coord2):
        '''
        On which axis occurs change of position
        :param coord1:
        :param coord2:
        :return:
        '''
        if coord1[0] == coord2[0]:
            return 'x'
        else:
            return 'y'

    res = []

    prev_axis = get_axis(route[0], route[1])
    prev_ind = 0
    for i in range(2, len(route)):
        cur_axis = get_axis(route[i - 1], route[i])
        if cur_axis != prev_axis:
            res.append(route[prev_ind:i])
            prev_axis = cur_axis
            prev_ind = i
    res.append(route[prev_ind:len(route)])
    return res
