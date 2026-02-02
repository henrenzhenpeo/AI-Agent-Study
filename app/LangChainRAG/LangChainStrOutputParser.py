from dotenv import load_dotenv

load_dotenv()

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import AIMessage

parser = StrOutputParser()

model = ChatTongyi(model="qwen3-max")

prompt = PromptTemplate.from_template(
    "我的邻居姓：{lastname}，刚生了{gender}，请起名，仅告知我名字无需其他内容。"
)

chain = prompt | model | parser | model | parser

res: AIMessage = chain.invoke({"lastname":"陈","gender":"男孩儿"})
print(res)
print(type(res))