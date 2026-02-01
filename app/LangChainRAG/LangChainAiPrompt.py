from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import PromptTemplate
from langchain_community.llms.tongyi import Tongyi

# zero-shot
# 1️⃣ 定义模板
prompt = PromptTemplate.from_template(
    "我的邻居姓{lastname}, 刚生了{gender}, 你帮我起个名字，简单回答。"
)
model = Tongyi(model="qwen-max")
# 2️⃣ 填充模板
# prompt_text = prompt.format(lastname="陈", gender="女儿")
#
# # 3️⃣ 初始化模型
# model = Tongyi(model="qwen-max")
#
# # 4️⃣ 调用模型
# res = model.invoke(input=prompt_text)
# print(res)
chain = prompt | model
res = chain.invoke(input={"lastname":"陈","gender":"儿子"})
print(res)