from langchain_gigachat.chat_models import GigaChat
from langgraph.prebuilt import create_react_agent

from core.config import GlobalConfig
from core.tools.calculator import BusinessSupport, Recommendations, DigitalMaturity


class AsyncChat:
    _model: GigaChat = None

    def __init__(self):
        self._model = self._initialize_model()

    @staticmethod
    def _initialize_model() -> GigaChat:
        return GigaChat(
            credentials=GlobalConfig["token"],
            scope="GIGACHAT_API_PERS",
            model="GigaChat-Pro",
            verify_ssl_certs=False
        )

    @property
    def model(self) -> GigaChat:
        return self._model


class AsyncAgent(AsyncChat):
    def __init__(self, tools: list, system_prompt: str):
        super().__init__()
        self._tools = tools
        self._system_prompt = system_prompt
        self.agent = create_react_agent(
            self._model,
            tools=self._tools,
            prompt=self._system_prompt
        )

    async def process_message(self, messages: list) -> str:
        response = await self.agent.ainvoke({"messages": messages})
        print(response["messages"][-1].content)
        return response["messages"][-1].content


GlobalAsyncAgent = AsyncAgent([BusinessSupport(), Recommendations(), DigitalMaturity()], "Ты ассистент для бизнеса, твоя задача помогать пользователям")
