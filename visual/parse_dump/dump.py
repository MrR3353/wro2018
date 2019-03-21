import json
import visual.config.parse as parse
import time
import var

path_config = "visual/config/config.json"
path_default_config = "visual/config/default_config.json"

def dump(keys, values):
    with open(path_config, 'r') as f:
        data = json.loads(f.read())
        for i in range(len(keys)):
            data[keys[i]] = values[i]
    with open(path_config, 'w') as f:
        json.dump(data, f)

def dump_all():
    dump(
        ["field_rob",
         "field_eva",
         "coord_rob",
         "coord_eva",
         "alpha_rob",
         "alpha_eva",
         "real_rob_coord",
         "real_eva_coord",
         "real_rob_alpha",
         "real_eva_alpha",
         "box_coords",
         "u_box_coords"],
        [parse.parse_field(var.rob.field),
         parse.parse_field(var.eva.field),
         [var.rob.coord[0] + 1,var.rob.coord[1] + 1],
         [var.eva.coord[0] + 1,var.eva.coord[1] + 1],
         var.rob.alpha,
         var.eva.alpha,
         [var.rob.real_coord[0] + 1,var.rob.real_coord[1] + 1],
         [var.eva.real_coord[0] + 1,var.eva.real_coord[1] + 1],
         var.rob.real_alpha,
         var.eva.real_alpha,
         var.box_coords,
         var.u_box_coords]
    )

def forever_dump_all():
    while True:
        dump_all()
        time.sleep(0.3)



    