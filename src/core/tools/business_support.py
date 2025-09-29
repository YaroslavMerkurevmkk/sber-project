from langchain_core.vectorstores.base import VectorStoreRetriever

from core.tools import RAGTool


class BusinessSupport(RAGTool):
    name: str = "Поддержка бизнеса"
    description: str = "Позволяет найти способы поддержки предприятий государством и тд."
    _retriever: VectorStoreRetriever = None

    def __init__(self):
        super().__init__()
        self._retriever = self.load_vectorstore("Поддержка бизнеса").as_retriever(search_type="similarity",
                                                                                  search_kwargs={"k": 3})
