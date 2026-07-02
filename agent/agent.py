from .session import AgentSession
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage
from prompts.system import SYSTEM_PROMPT
from .llm import LLM
from tool_registry import TOOLS

tool_map = {
    tool.name: tool for tool in TOOLS
}

class Agent:
    def __init__(self):
        self.session = AgentSession()
        self.llm = LLM()

    def run(self, prompt: str):
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
                    HumanMessage(content=prompt)
                    ]
        while True:
            ai_message = self.llm.invoke(messages)

            if not ai_message.tool_calls:
                return ai_message.content

            for tool_call in ai_message.tool_calls:
                tool = tool_map[tool_call["name"]]
                try:
                    tool_result = tool.invoke(tool_call['args'])
                    print("Executing tool:", tool_call["name"], "with args:", tool_call['args'])
                    print("Tool result:", tool_result)
                
                except Exception as e:
                    tool_result = {
                    "success": False,
                    "error": str(e)
                    }
                
                messages.append(ToolMessage(
                    content=str(tool_result),
                    tool_call_id = tool_call["id"]
                ))
                