import pymongo
import pandas as pd


'''通过配置文件获取mongodb链接'''
def get_MongoClient(config):
    db_config = config["database"]
    url = "mongodb://{}:{}@{}:{}".format(db_config["user"], db_config["password"], db_config["address"], db_config["port"])
    return pymongo.MongoClient(url)


'''获取查询结果的DataFrame'''
def get_find_df_result(collection, filter={}):
    return pd.DataFrame(list(collection.find(filter)))

