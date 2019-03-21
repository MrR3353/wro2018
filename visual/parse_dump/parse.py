import json # Used to read json format
import sys # Used to do system exit

import var # Used to change var data
 

def parse_all():
    '''
    parse_all - parse all start data
    '''

    var.base_field = parse_default_field()
    var.rob.real_coord, var.eva.real_coord = parse_default_coord()
    var.rob.real_alpha, var.eva.real_alpha = parse_default_alpha()
    var.box_coords = parse_box_coords()
    var.dump_coord = parse_dump_coord()

def parse_field(field):
    '''
    parse_field - turns field into json format
    '''

    coords = list(field.keys())
    min_x = sorted(coords)[0][0]
    min_y = sorted(coords)[0][1]
    
    field_parse = {}
    for coord, cell in field.items():
        coord_parse = str(coord[0] - min_x + 1) + str(coord[1] - min_y + 1)
        cell_parse = ""
        for i in range(4):
            if cell[i] == 1:
                if i == 0:
                    next_coord = coord_parse[0] + str(int(coord_parse[1]) + 1)
                    if next_coord in field_parse:
                        if "l" in field_parse[next_coord]:
                            pass
                        else:
                            cell_parse += "r"
                    else:
                        cell_parse += "r"
                    
                if i == 1:
                    next_coord = str(int(coord_parse[0]) + 1) + coord_parse[1]
                    if next_coord in field_parse:
                        if "t" in field_parse[next_coord]:
                           pass
                        else:
                            cell_parse += "b"
                    else:
                        cell_parse += "b"
                    
                if i == 2:
                    next_coord = coord_parse[0] + str(int(coord_parse[1]) - 1)
                    if next_coord in field_parse:
                        if "r" in field_parse[next_coord]:
                            pass
                        else:
                            cell_parse += "l"
                    else:
                        cell_parse += "l"
                if i == 3:
                    next_coord = str(int(coord_parse[0]) - 1) + coord_parse[1]
                    if next_coord in field_parse:
                        if "b" in field_parse[next_coord]:
                            pass
                        else:
                            cell_parse += "t"
                    else:
                        cell_parse += "t"
        field_parse[coord_parse] = cell_parse
    
    return field_parse


# Start parsers
def parse_default_field():
    '''
    parse_default_field -  base field parser
    '''

    with open("visual/config/default_config.json") as f:
        data = json.loads(f.read())
        if not "field" in data:
            print("No field in default__config.json")
            sys.exit(2)
        field = data["field"]
        field_ret = {}
        for coord, cell in field.items():
            cell_field = [0,0,0,0]
            coord_field = (int(coord[0]) - 1, int(coord[1]) - 1)
            if "r" in cell:
                cell_field[0] = 1
            else:
                coord_next = str(coord_field[0] + 1) + str(coord_field[1] + 2)
                if coord_next in field:
                    if "l" in field[coord_next]:
                        cell_field[0] = 1
            if "b" in cell:
                cell_field[1] = 1
            else:
                coord_next = str(coord_field[0] + 2) + str(coord_field[1] + 1)
                if coord_next in field:
                    if "t" in field[coord_next]:
                        cell_field[1] = 1
            if "l" in cell:
                cell_field[2] = 1
            else:
                coord_next = str(coord_field[0] + 1) + str(coord_field[1])
                if coord_next in field:
                    if "r" in field[coord_next]:
                        cell_field[2] = 1

            if "t" in cell:
                cell_field[3] = 1
            else:
                coord_next = str(coord_field[0]) + str(coord_field[1] + 1)
                if coord_next in field:
                    if "b" in field[coord_next]:
                        cell_field[3] = 1
            field_ret[coord_field] = cell_field
    return field_ret

def parse_default_coord():
    '''
    parse_default_coord - start real coordinates parser
    '''

    with open("visual/config/default_config.json", "r") as f:
        data = json.loads(f.read())
        if not ("real_rob_coord" in data or "real_eva_coord" in data):
            print("No real_coords in default_config.json")
            sys.exit(2)
        coord_rob = data["real_rob_coord"]
        coord_eva = data["real_eva_coord"]
        return (coord_rob[0] - 1, coord_rob[1] - 1), (coord_eva[0] - 1, coord_eva[1] - 1)
        
def parse_default_alpha():
    '''
    parse_default_alpha - start real alpha parser 
    '''

    with open("visual/config/default_config.json", "r") as f:
        data = json.loads(f.read())
        if not ("real_rob_alpha" in data or "real_eva_alpha" in data):
            print("No real_coords in default_config.json")
            sys.exit(2)
        alpha_rob = data["real_rob_alpha"]
        alpha_eva = data["real_eva_alpha"]
        return alpha_rob, alpha_eva

def parse_box_coords():
    '''
    parse_box_coords - start box coordinates parser
    '''

    with open("visual/config/default_config.json", "r") as f:
        data = json.loads(f.read())
        if not ("box_coords" in data):
            print("No box_coords in default_config.json")
            sys.exit(2)
        box_coords = data["box_coords"]
        return box_coords

def parse_dump_coord():
    '''
    parse_dump_coord - dump coord parser
    '''

    with open("visual/config/default_config.json", "r") as f:
        data = json.loads(f.read())
        if not ("dump_coord" in data):
            print("No real_coords in default_config.json")
            sys.exit(2)
        dump_coord = data["dump_coord"]
        return dump_coord