from langchain_core.vectorstores import VectorStoreRetriever

from core.tools import RAGTool


class DigitalMaturity(RAGTool):
    name: str = "Цифровая зрелость"
    description: str = ("Позволяет найти информацию о цифровой зрелости компаний."
                        "Помогает составить опрос пользователя для определения цифровой зрелости.")
    _retriever: VectorStoreRetriever = None

    def __init__(self):
        super().__init__()
        self._retriever = self.load_vectorstore("Цифровая зрелость").as_retriever(search_type="similarity",
                                                                                  search_kwargs={"k": 3})
