from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

llm = ChatOpenAI(
    model = "qwen-max-latest",
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key = SecretStr("sk-1e03921af5354973b776550886397a6b"),
    # stream = True,
)
# PromptTemplate 纯字符串的提示词模版
# 创建提示词模版
prompt_template= PromptTemplate.from_template("今天{something}真不错")
# 模版 + 变量 =》提示词
prompt = prompt_template.format(something = "天气")
print(prompt)

resp = llm.stream(prompt)

for chunk in resp:
    print(chunk.content, end="")