"""
知识库
"""
from dotenv import load_dotenv

load_dotenv()
import os

from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings

import config_data as config
import hashlib
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime

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
        # 如果文件夹存在则创建，如果不存在则跳过
        os.makedirs(config.persist_directory, exist_ok=True)
        self.chroma = Chroma(
            collection_name=config.collection_name,   # 数据库的表名
            embedding_function=DashScopeEmbeddings(model="text-embedding-v4"),
            persist_directory=config.persist_directory, # 数据库本地存储文件夹
        )    #向量存储的示例
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size, #分割后的文本段最大长度
            chunk_overlap = config.chunk_overlap, #连续文本段之间的字符重叠数量
            separators=config.separators, #自然段落划分的符号
            length_function=len, #使用py自带的len函数坐长度统计的依赖
        )   #文本分割器的对象

    def upload_by_str(self, data: str, filename):
        md5_hex = get_string_md5(data)
        if check_md5(md5_hex):
            return "[跳过]内容已经存在知识库中"

        # 确保 knowledge_chunks 一定被赋值
        if len(data) > config.max_split_char_number:
            knowledge_chunks = self.spliter.split_text(data)
        else:
            knowledge_chunks = [data]

        metadata = {
            "source": filename,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": "zzh"
        }

        self.chroma.add_texts(
            knowledge_chunks,
            metadatas=[metadata for _ in knowledge_chunks]
        )

        save_md5(md5_hex)

        return "[成功]内容已经成功载入向量库"


if __name__ == '__main__':

    service = KnowledgeBaseService()
    r = service.upload_by_str("张国荣","testfile")
    print(r)