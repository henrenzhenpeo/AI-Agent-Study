# langchain_community
from dotenv import load_dotenv
from langsmith import trace

load_dotenv()
from langchain_community.llms.tongyi import Tongyi

# qwen3-max 是chat模型，qwen-max是大语言模型
model= Tongyi(model = "qwen-max")

res = model.stream(input="你是谁？")


for chunk in res:
    print(chunk, end="",flush=True)