from dotenv import load_dotenv

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
    ("ai","万里悲秋常作客，艰难苦恨繁霜鬓"),
]

prompt_text = chat_prompt_tempt.invoke({"history": history_message}).to_string()
print(prompt_text)

model = ChatTongyi(model = "qwen3-max")

res = model.invoke(prompt_text)

print(res.content, type(res))