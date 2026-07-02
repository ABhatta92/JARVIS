from langchain_ollama import ChatOllama
from langchain_core.messages import BaseMessage
from tool_registry import TOOLS

class LLM:
    def __init__(self):
        self.model = ChatOllama(
            model="qwen3",
            reasoning=False
        ).bind_tools(TOOLS)

    def invoke(self, messages: list[BaseMessage]):
        return self.model.invoke(messages)