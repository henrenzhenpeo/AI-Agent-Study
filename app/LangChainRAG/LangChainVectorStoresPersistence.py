from dotenv import load_dotenv

load_dotenv()
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders.csv_loader import CSVLoader

# Chroma 向量数据库(轻量级)
# 确保 langchain-chroma chromadb
vector_store = Chroma(
    collection_name="test",
    embedding_function=DashScopeEmbeddings(),
    persist_directory="./chromadb"
)
#
# loader = CSVLoader(
#     file_path="./data/info.csv",
#     encoding="utf-8",
#     source_column="source",
# )
#
# documents = loader.load()
#
# # 向量存储的 新增，删除，检索
# vector_store.add_documents(
#     documents=documents,
#     ids=["id"+str(i) for i in range(1,len(documents)+1)]
# )

vector_store.delete(["id1","id2"])
res = vector_store.similarity_search(
    "怕赢会输吗",
    3
)

print(res)

