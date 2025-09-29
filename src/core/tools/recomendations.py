from langchain_core.vectorstores import VectorStoreRetriever

from core.tools import RAGTool


class Recommendations(RAGTool):
    name: str = "Рекомендации"
    description: str = "Позволяет найти рекомендации по внедрению IT-решений в бизнесе и т.д."
    _retriever: VectorStoreRetriever = None

    def __init__(self):
        super().__init__()
        self._retriever = self.load_vectorstore("Рекомендации").as_retriever(search_type="similarity",
                                                                             search_kwargs={"k": 3})
