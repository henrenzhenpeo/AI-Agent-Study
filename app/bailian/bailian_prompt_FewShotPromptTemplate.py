from sys import prefix

from langchain_core.prompts import ChatPromptTemplate, ChatMessagePromptTemplate, FewShotPromptTemplate, PromptTemplate
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

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
# 模版 + 变量 =》提示词
prompt = chat_prompt_template.format_messages(
    role = "编程",
    domain = "区块链开发",
    question = "你擅长什么？"
)
print(prompt)



examples_template = "输入：{input}\n输出：{output}"
examples = [
    {"input":"将'hello world'翻译成中文","output":"你好世界"},
    {"input":"将'Goodbye'翻译成中文","output":"再见"},
]
few_shot_prompt_template = FewShotPromptTemplate(
    examples = examples,
    example_prompt = PromptTemplate.from_template(examples_template),
    prefix="请将以下英文翻译成中文",
    suffix = "输入：{text}\n输出：",
    input_variables = ["text"],
)

print(few_shot_prompt_template)

prompt = few_shot_prompt_template.format(text = "Thank you!")
print(prompt)

# resp = llm.stream(prompt)

chain = few_shot_prompt_template | llm

resp = chain.stream(input={"text":"white!"})

for chunk in resp:
    print(chunk.content, end="")