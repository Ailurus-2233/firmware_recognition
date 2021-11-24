import hashlib
import subprocess
import os

from numpy import inf


# 获取文件的md5
def get_file_md5(file):
    with open(file, 'rb') as f:
        m = hashlib.md5()
        while True:
            data = f.read(10240)
            if not data:
                break
            m.update(data)
        return m.hexdigest()


# 获取文件大小
def get_file_size(file):
    fsize = os.path.getsize(file)
    fsize /= (1024 * 1024)
    return round(fsize, 5)

# 执行terminal指令并返回结果
def shell_res(shell):
    res = ""
    p = subprocess.Popen(
        shell, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    for line in p.stdout.readlines():
        try:
            res = res + line.decode("utf-8")
        except:
            print(shell, "====", line)
    retvel = p.wait()
    return res, retvel


# 比对strings指令返回数据，推断版本信息
def match_models_info(path, file_name, models):
    shell = "strings '{}'".format(path)
    res, flag = shell_res(shell)
    if flag == 0:
        res = res.split("\n")
        res.insert(0, file_name)
        for info in res:
            for model in models:
                info = info.replace("-", "")
                info = info.replace("_", "")
                if model in info.upper():
                    return model

    return None
