from dotenv import load_dotenv

load_dotenv()

from langchain_community.document_loaders.csv_loader import CSVLoader

loader = CSVLoader(
    file_path = "./data/stu.csv",
    csv_args={
      "delimiter": ",",
      "quotechar": '"',
        # 表头
      "fieldnames": ['A','B','C','D']
      # "skipinitialspace": True,
      # "quoting": None
    },
    encoding = "utf-8",
)

# documents = loader.load()
#
# for document in documents:
#     print(type(document), document)


# 懒加载 /lazy_load()
for document in loader.lazy_load():
    print(type(document), document)