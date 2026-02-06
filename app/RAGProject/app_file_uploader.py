"""
基于Streamlit 完成web页面上传服务

Streamlit : 当web页面代码元素发生变化的时候，则代码重新执行一遍
"""
import time

import streamlit as st
from knowledge_base import KnowledgeBaseService

# 添加网页标题  streamlit run 文件名
st.title("知识库更新服务")

# file_uploader
uploaded_file = st.file_uploader(
    "请上传TXT文件",
    type=["txt"],
    accept_multiple_files=False, #False 表示仅接受一个文件的上传
)

# session_state 就是一个字典
# if "counter" not in st.session_state:
#     st.session_state["counter"] = 0

if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()


if uploaded_file is not None:
    # 提取文件的信息
    file_name = uploaded_file.name
    file_type = uploaded_file.type
    file_size = uploaded_file.size / 1024 #kb

    st.subheader(f"文件名：{file_name}")
    st.write(f"格式：{file_type} | 大小：{file_size:.2f} KB")

    # get_value ->bytes -> decode('UTF-8')
    text = uploaded_file.getvalue().decode("utf-8")

    with st.spinner("载入知识库中。。。"):
        time.sleep(1)
        result = st.session_state["service"].upload_by_str(text, file_name)
        st.write(result)

#     st.write(text)
#
#     st.session_state["counter"] += 1
#
# print(f'上传了{st.session_state["counter"]}个文件')