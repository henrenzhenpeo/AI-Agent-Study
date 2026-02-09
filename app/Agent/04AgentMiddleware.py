from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import (
    before_agent, after_agent,
    before_model, after_model,
    wrap_model_call, wrap_tool_call
)
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool
from dotenv import load_dotenv
from langgraph.runtime import Runtime

load_dotenv()

@tool(description="查询天气,传入城市名称字符串，返回字符串天气信息")
def get_weather(city: str) -> str:
    return f"{city}天气:晴天"


# ========== Agent 生命周期 ==========
@before_agent
def log_before_agent(state: AgentState, runtime: Runtime) -> None:
    print(f"[before agent] agent 启动，消息数: {len(state['messages'])}")

@after_agent
def log_after_agent(state: AgentState, runtime: Runtime) -> None:
    print(f"[after agent] agent 结束，消息数: {len(state['messages'])}")


# ========== Model 生命周期 ==========
@before_model
def log_before_model(state: AgentState, runtime: Runtime) -> None:
    print(f"[before model] 模型即将调用，消息数: {len(state['messages'])}")

@after_model
def log_after_model(state: AgentState, runtime: Runtime) -> None:
    print(f"[after model] 模型调用结束，消息数: {len(state['messages'])}")


# ========== Hook ==========
@wrap_model_call
def model_call_hook(request, handler):
    print("模型被调用")
    return handler(request)


@wrap_tool_call
def monitor_tool(request, handler):
    print(f"工具执行：{request.tool_call['name']}")
    print(f"工具参数：{request.tool_call['args']}")
    return handler(request)


# 关键：middleware 里只放 middleware 实例（已装饰函数）
agent = create_agent(
    model=ChatTongyi(model="qwen3-max"),
    tools=[get_weather],
    middleware=[
        log_before_agent,
        log_after_agent,
        log_before_model,
        log_after_model,
        model_call_hook,
        monitor_tool,
    ],
)

res = agent.invoke({
    "messages": [
        {"role": "user", "content": "深圳今天天气如何呀，如何穿衣"}
    ]
})

print("***********\n", res)
