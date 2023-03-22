import os.path


# 存储文件
def save_file(path, text):
    if os.path.isfile(path):
        os.remove(path)

    f = open(path, 'w')
    # 写入文件
    f.write(text)
    f.close()