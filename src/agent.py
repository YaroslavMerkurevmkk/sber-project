from langchain_gigachat.chat_models import GigaChat
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

from config import GlobalConfig


class Chat:
    _model: GigaChat = None
    _model_with_tools: GigaChat = None

    def __init__(self):
        self._model = self._initialize_model()

    def _initialize_model(self) -> GigaChat:
        return GigaChat(
            credentials=GlobalConfig["token"],
            scope="GIGACHAT_API_PERS",
            model="GigaChat-Pro",
            verify_ssl_certs=False,
        )

    @property
    def model(self) -> GigaChat:
        return self._model


class Agent(Chat):
    def __init__(self, tools: list, system_prompt: str):
        super().__init__()

        self.agent = create_react_agent(
            self._model,
            tools=tools,
            checkpointer=MemorySaver(),
            prompt=system_prompt,
        )

    def invoke(self, message, thread_id: str):
        return self.agent.invoke(
            message, config={"configurable": {"thread_id": thread_id}}
        )