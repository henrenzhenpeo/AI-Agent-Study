from dotenv import load_dotenv

load_dotenv()

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = TextLoader(
    "./data/中水测试用例.txt",
    encoding="utf-8",
)

docs = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n","\n","}","{","。",".",",","!","?"," ",""],
    length_function=len
)

split_doc = splitter.split_documents(docs)
print(len(split_doc))
for doc in split_doc:
    print("="*20)
    print(doc)
    print("="*20)