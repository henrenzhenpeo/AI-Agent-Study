from dotenv import load_dotenv
from langchain_core.runnables import RunnableSerializable

load_dotenv()

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi

chat_prompt_tempt = ChatPromptTemplate.from_messages(
    [
        ("system","你是一个边塞诗人，可以作诗"),
        MessagesPlaceholder("history"),
        ("human","请再来一首唐诗")
    ]
)

history_message = [
    ("human","你是一个边塞诗人，可以作诗"),
    ("ai","大漠孤烟直，长河落日圆"),
    ("human","好诗再来一首"),
    ("ai","黄沙百战穿金甲，不破楼兰终不还"),
]

model = ChatTongyi(model = "qwen3-max")

chain: RunnableSerializable = chat_prompt_tempt | model

print(type(chain))

res = chain.invoke({"history":history_message})
print(res.content)

for chunk in chain.stream({"history":history_message}):
    print(chunk.content, end="",flush=True)
