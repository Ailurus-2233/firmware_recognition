import json

'''global '''
config_path = "./config.conf"


''' load config file '''
with open(config_path, "r") as f:
    config = json.load(f)

