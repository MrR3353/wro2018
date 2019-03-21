'''
This is a config file, where you can set the required values and parameters
'''

# Robots
eva = None
rob = None

# Operating mode of the program. If dbg = false, then classic mode working
dbg = False
# Flag which defines that visual module is working. If dbg = True, visual must = True
visual = False

# count of unknown boxes on map at now
# decrement at high level
unknown_boxes = 1

sync = False    # Moving synchronously
who_moves = 'Eva'   # do eva moves?
met = False    # Robots meets before?

reset_point = (5, 5)

# known boxes coords
# remove ONLY in robot.run().box_collection()
box_coords = [(1, 1), (5, 3)]

# Unknown boxes coords (Only dbg)
u_box_coords = []

# full map
base_field = {(0, 0): [0, 1, 1, 1], (0, 1): [1, 0, 0, 1], (0, 2): [1, 0, 1, 1], (0, 3): [0, 0, 1, 1], (0, 4): [0, 1, 0, 1], (0, 5): [1, 0, 0, 1], (0, 6): [1, 0, 1, 1], (0, 7): [1, 0, 1, 1], (1, 0): [1, 0, 1, 1], (1, 1): [0, 0, 1, 0], (1, 2): [0, 1, 0, 0], (1, 3): [1, 0, 0, 0], (1, 4): [1, 0, 1, 1], (1, 5): [0, 0, 1, 0], (1, 6): [0, 1, 0, 0], (1, 7): [1, 0, 0, 0], (2, 0): [0, 1, 1, 0], (2, 1): [1, 0, 0, 0], (2, 2): [1, 0, 1, 1], (2, 3): [0, 0, 1, 0], (2, 4): [0, 1, 0, 0], (2, 5): [1, 0, 0, 0], (2, 6): [1, 0, 1, 1], (2, 7): [1, 0, 1, 0], (3, 0): [1, 0, 1, 1], (3, 1): [0, 0, 1, 0], (3, 2): [0, 1, 0, 0], (3, 3): [1, 0, 0, 0], (3, 4): [1, 0, 1, 1], (3, 5): [0, 0, 1, 0], (3, 6): [0, 1, 0, 0], (3, 7): [1, 0, 0, 0], (4, 0): [0, 1, 1, 0], (4, 1): [1, 0, 0, 0], (4, 2): [1, 0, 1, 1], (4, 3): [0, 0, 1, 0], (4, 4): [0, 1, 0, 0], (4, 5): [1, 0, 0, 0], (4, 6): [1, 0, 1, 1], (4, 7): [1, 0, 1, 0], (5, 0): [1, 0, 1, 1], (5, 1): [0, 0, 1, 0], (5, 2): [0, 1, 0, 0], (5, 3): [1, 0, 0, 0], (5, 4): [1, 0, 1, 1], (5, 5): [0, 0, 1, 0], (5, 6): [0, 1, 0, 0], (5, 7): [1, 0, 0, 0], (6, 0): [0, 1, 1, 0], (6, 1): [1, 0, 0, 0], (6, 2): [1, 0, 1, 1], (6, 3): [0, 0, 1, 0], (6, 4): [0, 1, 0, 0], (6, 5): [1, 0, 0, 0], (6, 6): [1, 0, 1, 1], (6, 7): [1, 0, 1, 0], (7, 0): [1, 1, 1, 1], (7, 1): [0, 1, 1, 0], (7, 2): [0, 1, 0, 0], (7, 3): [1, 1, 0, 0], (7, 4): [1, 1, 1, 1], (7, 5): [0, 1, 1, 0], (7, 6): [0, 1, 0, 0], (7, 7): [1, 1, 0, 0]}

#   Defines in init:
# 4 fields: 0,90,180,270 degrees
field = {}

# coords, where i wasn't
# if robot localized we must remove cells from var.was_not on each step of localized robot
# also we clear this field after localization
was_not = []  # list(base_field.keys())

# cells that i can visit. It is taken into account that robots always connected in the field
available_cells = []  # list(base_field.keys())