from typing import Sequence

from dotenv import load_dotenv
from langchain_community.chat_models import ChatTongyi
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory

load_dotenv()

import os, json
from langchain_core.messages import message_to_dict, messages_from_dict, BaseMessage
from langchain_core.chat_history import BaseChatMessageHistory

# message_to_dict 单个消息对象（BaseMessage类实例） -> 字典
# message_from_dict: [字典，字典....] -> [消息，消息...。]
# AIMessage,HumanMessage,SystemMessage 都是BaseMessage子类

class FileChatMessageHistory(BaseChatMessageHistory):

    def __init__(self, session_id, storage_path):
        self.session_id = session_id
        self.storage_path = storage_path
        # 完整的文件路径
        self.file_path = os.path.join(self.storage_path, self.session_id)

        # 确保文件夹是存在
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        # Sequence 类似于 list
        all_messages = list(self.messages)
        all_messages.extend(messages)

        # 将数据同步写入到本地文件中
        # 类对象写入文件 -> 二进制
        # new_messages = []
        # for message in all_messages:
        #     d = message_to_dict(message)
        #     new_messages.append(d)

        new_messages = [message_to_dict(message) for message in all_messages]
        # 讲数据写入文件
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(new_messages, f, ensure_ascii=False, indent=4)

    @property  # @property 将messages方法变成成员属性
    def messages(self) -> list[BaseMessage]:
        # 当前文件内: list[字典]
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                messages_data = json.load(f)  # 返回值 list[字典]
                return messages_from_dict(messages_data)
        except FileNotFoundError:
            return []

    def clear(self) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=4)



model = ChatTongyi(model="qwen3-max")

# prompt = PromptTemplate.from_template(
#     "你需要根据会话的历史回应用户问题，对话历史：{chat_history}，用户提问：{input}，请回答"
# )

prompt = ChatPromptTemplate.from_messages(
    [
        ("system","你需要根据会话历史回应用户的问题。对话历史："),
        MessagesPlaceholder("chat_history"),
        ("human","请回答如下问题：{input}")
    ]
)

str_parser = StrOutputParser()


def print_prompt(full_prompt):
    print("="*20, full_prompt.to_string(),"="*20)
    return full_prompt


base_chain = prompt | print_prompt | model | str_parser

def get_history(session_id):
    return FileChatMessageHistory(session_id=session_id, storage_path="./chat_history")



# 创建一个新的链，对原有链增强功能：自动附加历史消息
conversation_chain = RunnableWithMessageHistory(
    base_chain,  #被增量的原有chain
    get_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

if __name__ == '__main__':

    session_config = {
        "configurable":{
            "session_id":"00011",
        }
    }

    # res = conversation_chain.invoke({"input":"小波有两个猫"},session_config)
    # print("第一次执行：",res)
    #
    # res = conversation_chain.invoke({"input":"小撒有两个猫"},session_config)
    # print("第二次执行：",res)

    res = conversation_chain.invoke({"input":"总共有几只猫"},session_config)
    print("第三次执行：",res)