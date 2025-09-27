from typing import Optional

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.tools import BaseTool
from langchain_core.vectorstores.base import VectorStoreRetriever


class BusinessSupport(BaseTool):
    name: str = "Поддержка бизнеса"
    description: str = "Позволяет найти способы поддержки предприятий государством и тд."
    _retriever: VectorStoreRetriever = None

    def __init__(self):
        super().__init__()
        loader = DirectoryLoader("/home/ghost/Documents/projects/sber-project/data/Поддержка бизнеса/", glob="*.md",
                                 loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"})
        docs = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        splits = splitter.split_documents(docs)

        embedding = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        vectorstore = Chroma.from_documents(splits, embedding)
        self._retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})

    def _run(self, query: str) -> Optional[str]:
        results = self._retriever.get_relevant_documents(query)
        return "\n\n".join([doc.page_content for doc in results])

    async def _arun(self, query: str) -> Optional[str]:
        results = await self._retriever.ainvoke(query)
        return "\n\n".join([doc.page_content for doc in results])
