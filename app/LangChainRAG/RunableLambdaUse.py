from dotenv import load_dotenv

load_dotenv()

from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.runnables import RunnableLambda

str_parser = StrOutputParser()

model = ChatTongyi(model="qwen3-max")

first_prompt = PromptTemplate.from_template(
    "我的邻居姓：{lastname}，刚生了{gender}，请起名，仅告知我名字无需其他内容。并封装为JSON格式返回给我，要求key是name，value就是你起的名字，请严格遵守格式要求"
)

second_prompt = PromptTemplate.from_template(
    "姓名：{name}，请帮我解析含义。"
)

# my_func = RunnableLambda(lambda ai_msg: {"name": ai_msg.content})

chain = first_prompt | model | (lambda ai_msg: {"name": ai_msg.content}) | second_prompt | model | str_parser

for chunk in chain.stream({"lastname":"张", "gender": "男孩"}):
    print(chunk, end="", flush=True)