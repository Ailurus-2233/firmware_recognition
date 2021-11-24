import pymongo
import pandas as pd


# 通过配置文件获取mongodb链接
def get_MongoClient(config):
    db_config = config["database"]
    url = "mongodb://{}:{}@{}:{}".format(
        db_config["user"], db_config["password"], db_config["address"], db_config["port"])
    return pymongo.MongoClient(url)


# 获取查询结果的DataFrame
def df_find_result(collection, filter={}):
    return pd.DataFrame(list(collection.find(filter)))


# 获得特定厂商的库中的产品列表
def get_models_by_vendor(collection, vendor):
    df = df_find_result(collection, {"vendor": vendor})
    return list(df["model"].values)


# 判断数据库中是否有这个文件信息
def is_have_firmware(collection, file_md5, vendor):
    df = df_find_result(
        collection, {"match_vendor": vendor, "firmware_file_md5": file_md5})
    return len(df.values) > 0


# 插入一条固件完整信息
def add_one_firmware_info(colletion, firmware_name, vendor, model, path, size, md5):
    new_info = {
        "firmware_file_name": firmware_name,
        "firmware_file_size": size,
        "match_vendor": vendor,
        "match_product": model,
        "firmware_file_path": path,
        "firmware_file_md5": md5
    }
    colletion.insert_one(new_info)


# 修改目标固件的产品型号信息
def update_firmware_model(collection, file_md5, model):
    arm_info = {"firmware_file_md5": file_md5}
    new_values = {"$set": {
        "match_product": model
    }}
    collection.update_one(arm_info, new_values)
