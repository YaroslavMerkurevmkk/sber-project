from typing import Optional

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_core.tools import BaseTool
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from core.config import GlobalConfig


class RAGTool(BaseTool):
    _retriever: VectorStoreRetriever = None

    @staticmethod
    def load_vectorstore(data: str) -> Chroma:
        loader = DirectoryLoader(GlobalConfig["data_dir"] / data, glob="*.md",
                                 loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"})
        docs = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        splits = splitter.split_documents(docs)

        embedding = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        return Chroma.from_documents(splits, embedding)

    def _run(self, query: str) -> Optional[str]:
        results = self._retriever.get_relevant_documents(query)
        return "\n\n".join([doc.page_content for doc in results])

    async def _arun(self, query: str) -> Optional[str]:
        results = await self._retriever.ainvoke(query)
        return "\n\n".join([doc.page_content for doc in results])
