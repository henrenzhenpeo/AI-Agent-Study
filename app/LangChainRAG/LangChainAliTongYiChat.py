# langchain_community
from dotenv import load_dotenv
from langchain_classic.chains.question_answering.map_reduce_prompt import messages
from sqlalchemy.sql.functions import count

from app.LangChainRAG.LangChainAliTongYi import model

load_dotenv()
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage

# 得到模型对象
model = ChatTongyi(model = "qwen3-max")

messages = [
    SystemMessage(content="你是一个边塞诗人"),
    HumanMessage(content="写一首唐诗"),
    AIMessage(content="醉里挑灯看剑，梦回吹角连营"),
    HumanMessage(content="按照上一个的回复写一首诗")
]

res = model.stream(input=messages)

for chunk in res:
    print(chunk.content,end="",flush=True)