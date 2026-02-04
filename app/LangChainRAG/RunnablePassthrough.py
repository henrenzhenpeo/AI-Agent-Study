
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough

from app.LangChainRAG.LangChainVectorStoresPrompt import print_prompt

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

# langchain 种向量存储对象，有一个方法，as_retriever ，可以返回一个Runnable 接口的子类实例对象
retriever = vector_store.as_retriever(search_kwargs={"k": 2})

# chain
# chain = retriever | prompt | model | StrOutputParser()
def format_func(docs: list[Document]):
    if not docs:
        return "无相关参考资料"

    formatted_str = "["
    for doc in docs:
        formatted_str += doc.page_content
    formatted_str += "]"

    return formatted_str

chain = (
    {"input": RunnablePassthrough(), "content": retriever | format_func} | prompt | print_prompt | model | StrOutputParser()
)

chain.invoke(input_text)


"""
retriever:
    - 输入：用户的提问 str
    - 输出：向量库的检索结果 list[Document]
prompt:
    - 输入：用户的提问 + 向量库的检索结果  dict
    - 输出：完整的提示词 PromptValue
"""

