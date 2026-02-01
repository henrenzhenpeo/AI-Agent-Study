# langchain_community
from dotenv import load_dotenv

load_dotenv()
from langchain_community.llms.tongyi import Tongyi

# qwen3-max 是chat模型，qwen-max是大语言模型
model= Tongyi(model = "qwen-max")

res = model.invoke(input="你是谁？")

print(res)