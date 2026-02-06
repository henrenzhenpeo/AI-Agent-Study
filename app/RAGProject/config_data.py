
md5_path = "./md5.txt"


# Chroma
collection_name = "rag"
persist_directory = "./chroma_db"

# spliter
chunk_size = 1024
chunk_overlap = 1024
separators = ["\n\n","\n","}","{","。",".",",","!","?"," ",""]
max_split_char_number = 1024   # 文本分割的阈值


# 相似度检索的阈值
similarity_threshold = 1       # 检索返回匹配后的数量

embedding_model_name = "text-embedding-v4"
chat_model_name = "qwen3-max"

# session id 配置
session_config = {
    "configurable": {
        "session_id": "zzh",
    }
}