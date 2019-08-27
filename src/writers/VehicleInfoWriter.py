import json


def generate_vehicle_info(file_path, vehicle):
    with open(file_path + "/vehicle_info.json", "w") as file:
        json.dump(vehicle.__dict__, file)
