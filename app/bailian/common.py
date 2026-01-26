from langchain_core.prompts import ChatPromptTemplate, ChatMessagePromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from pydantic import SecretStr, BaseModel, Field

llm = ChatOpenAI(
    model = "qwen-max-latest",
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key = SecretStr("sk-1e03921af5354973b776550886397a6b"),
    # stream = True,
)

system_message_template = ChatMessagePromptTemplate.from_template(
    template="你是一位{role}专家，擅长回答{domain}领域的问题",
    role = "system"
)

human_message_template = ChatMessagePromptTemplate.from_template(
    template="用户问题{question}",
    role = "user",
)

# PromptTemplate 纯字符串的提示词模版
# 创建提示词模版
chat_prompt_template = ChatPromptTemplate.from_messages([
    system_message_template,
    human_message_template,
])


class AddInputArgs(BaseModel):
    a: int = Field(description="first number")
    b: int = Field(description="second number")


@tool(
    description="add two numbers",
    args_schema=AddInputArgs,
    return_direct=True,
)
def add(a, b):
    """add two numbers"""
    return a + b


def create_calc_tools():
    return [add]


calc_tools = create_calc_tools()