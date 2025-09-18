from typing import Optional

from langchain_core.tools import BaseTool


class MyCalculator(BaseTool):
    name: str = "calculator"
    description: str = "Вычисляет простые арифметические выражения"

    def __init__(self):
        super().__init__()

    def _run(self, query: str) -> Optional[str]:
        try:
            result = eval(query)
            return str(result)
        except Exception as e:
            return f"Ошибка: {e}"

    async def _arun(self, query: str) -> Optional[str]:
        return self._run(query)