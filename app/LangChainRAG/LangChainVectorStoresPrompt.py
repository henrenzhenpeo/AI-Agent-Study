from dotenv import load_dotenv

load_dotenv()
from langchain_community.chat_models import ChatTongyi
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

model = ChatTongyi(model="qwen3-max")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system","以我提供的已知参考资料为主,简洁和专业的回答用户问题。参考资料:{content}"),
        ("user","用户提问:{input}")
    ]
)

vector_store = InMemoryVectorStore(embedding=DashScopeEmbeddings(model="text-embedding-v4"))

vector_store.add_texts(["股票就是要实时分析","炒股就是要满仓猛干，技术分析，频繁操作","mcd5就是很好的技术分析手段"])

input_text = "怎么炒股？"

result = vector_store.similarity_search(input_text,2)
reference_text = "["
for doc in result:
    reference_text += doc.page_content
reference_text += "]"

# print(reference_text)

def print_prompt(prompt):
    print(prompt.to_string)
    print("="*20)
    return prompt

chain = prompt | print_prompt | model | StrOutputParser()

res = chain.invoke({"input": input_text,"content": reference_text})
print(res)