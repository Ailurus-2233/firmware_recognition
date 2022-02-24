import json
import argparse
import numbers
import os
from pathlib import Path
from tqdm import tqdm

from utils import data, file


def main(args):

    os.chdir("../")

    ''' load config file '''
    with open(args.config_file, "r") as f:
        config = json.load(f)

    '''init mongodb client'''
    client = data.get_MongoClient(config)

    '''get file list & match info'''
    root_folder = Path(args.firmware_folder)
    folders = os.listdir(root_folder)
    index = 0
    for folder in tqdm(folders):
        index += 1
        print(index, folder)
        if index < args.start or index > args.end:
            os.system("clear")
            continue
        if folder in ["diankeyuan_firmware", "horner_automation"]:
            os.system("clear")
            continue
        if folder == "TP-LINK":
            vendor = "TPLINK"
        vendor = folder.upper()
        models = data.df_find_result(client["CIN"]["product"])
        models = list(models["model"][models["vendor"] == vendor].values)
        models = [i for i in models if i != None]
        models.sort(key=lambda i: len(i), reverse=True)
        files = os.listdir(root_folder/folder)
        for f in tqdm(files):
            fp = root_folder/folder/f
            if os.path.isdir(fp):
                continue
            model = file.match_models_info(fp, f, models)
            md5 = file.get_file_md5(fp)
            if data.is_have_match_product(client["CIN"]["firmware"], md5):
                continue
            if model != None and not args.test:
                if data.is_have_firmware(client["CIN"]["firmware"], md5, vendor):
                    data.update_firmware_model(
                        client["CIN"]["firmware"], md5, model)
                else:
                    data.add_one_firmware_info(
                        client["CIN"]["firmware"], f, vendor, model, str(fp)[5:], file.get_file_size(fp), md5)
            elif args.test:
                with open(args.log_file, "a", encoding='UTF-8') as lf:
                    lf.write("[test]: {},{},{}\n".format(f, vendor, model))
            else:
                with open(args.log_file, "a", encoding='UTF-8') as lf:
                    lf.write("[fail]: {},{}, None\n".format(f, vendor))
                if not data.is_have_firmware(client["CIN"]["firmware"], md5, vendor):
                    data.add_one_firmware_info(
                        client["CIN"]["firmware"], f, vendor, None, str(fp)[5:], file.get_file_size(fp), md5)
        os.system("clear")


if __name__ == "__main__":
    args = argparse.ArgumentParser(
        description='firmware model recognition tools')
    args.add_argument("-ff", "--firmware-folder", type=str,
                      help="The folder where the firmware is stored")
    args.add_argument("-v", "--vendor", type=str, 
                      help="The vendor of firmwares")
    args.add_argument("-cf", "--config-file", type=str, default="./config.conf",
                      help="The config file of tools")
    args.add_argument("-lf", "--log-file", type=str, 
                      default="./log/fr_tools.log", help="The log file of tools")
    args.add_argument("-t", "--test", action="store_true",
                      default=False, help="Test label")
    args.add_argument("-s", "--start", type=int, help="Start step")
    args.add_argument("-e", "--end", type=int, help="end step")                  
    main(args.parse_args())
