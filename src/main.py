from pprint import pprint

from langchain_core.messages import HumanMessage

from agent import Agent
from tools.calculator import MyCalculator


def main() -> None:
    agent = Agent(
        tools=[MyCalculator()],
        system_prompt="Ты помощник, который может использовать калькулятор для вычисления "
                      "простых арифметических выражений. Использовать можно только калькулятор для вычислений, "
                      "переданный тебе в инструментах")

    while True:
        try:
            response = agent.invoke(HumanMessage(content=input("Введите сообщение: ")), "testthread")
            pprint(response["messages"][-1].content)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
