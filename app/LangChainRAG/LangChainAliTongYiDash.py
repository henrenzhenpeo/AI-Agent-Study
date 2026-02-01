# langchain_community
from dotenv import load_dotenv

load_dotenv()
from langchain_community.embeddings import DashScopeEmbeddings

# DashScopeEmbeddings 默认使用text-v1的模型
embed = DashScopeEmbeddings()

print(embed.embed_query("我喜欢你"))
print(embed.embed_documents(['我喜欢你','我喜欢吃炸鸡腿']))