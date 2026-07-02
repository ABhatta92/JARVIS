from .workspace import Workspace

class AgentSession:
    def __init__(self):
        self.workspace = Workspace()
        self.logs = []
        self.chat_history = []