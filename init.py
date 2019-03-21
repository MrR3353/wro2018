import sys
import _thread

import var
import robot
import logic.algo as logic
import visual.parse_dump.dump as dump
import visual.parse_dump.parse as parse


'''
init.py - File if which the initialization occurs.
1. Checking command-line arguments
2. Declaration robots
3. Check config
4. Start parallel dump all
5. Getting fields
6. Checking connection
7. ...
'''

# Checking command-line arguments 
if len(sys.argv) > 1:
    print(sys.argv[1])
    if sys.argv[1] == "-d":
        var.classic = True
        var.visual = True
    elif sys.argv[1] == "-v":
        var.visual = True
    else:
        print("WRONG MODE")
        sys.exit(1)
else:
    var.classic = True

# Declaration robots
var.eva = robot.Robot(ip="192.168.43.36")
var.rob = robot.Robot(ip="192.168.43.166")

# Check config 
parse.parse_all()

# Start parallel dump all
if var.visual:
    _thread.start_new_thread(dump.forever_dump_all, ())

# Getting fields
for angle in (0, 90, 180, 270):
    var.field[angle] = logic.shift_field(var.base_field, angle)

#   Checking connection
#   TODO: Add connection check

