"""
知识库
"""
import os
import config_data as config
import hashlib

def check_md5(md5_str: str):
    # 检查传入的md5字符串是否已经被处理过了
    if not os.path.exists(config.md5_path):
        # if 进入表示文件不存在，那么就是没有处理过这个md5
        open(config.md5_path, 'w', encoding='UTF-8').close()
        return False
    else:
        for line in open(config.md5_path, 'r', encoding='UTF-8').readlines():
            line = line.strip()
            if md5_str == line:
                return True
        return False

def save_md5(md5_str: str):
    # 将传入的md5字符串，记录到文件内保存
    with open(config.md5_path, 'a', encoding='UTF-8') as f:
        f.write(md5_str + '\n')

def get_string_md5(input_str: str, encoding='utf-8'):
    # 将传入的字符串转换为md5字符串
    # 将字符串转换为bytes字节数组
    str_bytes= input_str.encode(encoding=encoding)

    # 创建md5对象
    md5 = hashlib.md5()        # 得到md5对象
    md5.update(str_bytes)      # 更新内容
    md5_hex = md5.hexdigest()  # 得到md5的十六进制字符串
    return md5_hex

class KnowledgeBaseService(object):
    def __init__(self):
        self.chroma = None    #向量存储的示例
        self.spliter = None   #文本分割器的对象

    def upload_file(self, data, filename):
        # 将传入的字符串，进行向量化，存入向量数据库中
        pass

if __name__ == '__main__':
    save_md5("b50c94280f95513ec56f1e0d989365fd")
    print(check_md5("b50c94280f95513ec56f1e0d989365fd"))
    # r1 = get_string_md5("张国荣")
    # r2 = get_string_md5("张国荣2")
    # r3 = get_string_md5("张国荣3")
    #
    # print(r1)
    # print(r2)
    # print(r3)