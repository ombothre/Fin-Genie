from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.utilities import PythonREPL
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from langchain_core.tools import tool
from typing import Annotated
from config import utils
import pandas as pd

GOOGLE_API_KEY = utils.GOOGLE_API_KEY

class AiAgent:
    def __init__(self, model: str):
        self.llm = ChatGoogleGenerativeAI(
            model=model,
            temperature=0.2,
            max_tokens=None,
            timeout=None,
            max_retries=3,
        )
        self.repl = PythonREPL()

    def setup_agent(self, df: pd.DataFrame, metadata) -> AgentExecutor:
        self.repl.globals["df"] = df

        @tool
        def python_repl(
            code: Annotated[str, "The python code to execute code"]
        ):
            """Execute python code and return results."""
            try:
                result = self.repl.run(code)
            except BaseException as e:
                return f"Failed to execute. Error: {repr(e)}"
            return (
                f"Successfully executed:\n```python\n{code}\n```\nStdout: {result}"
                + "\n\nIf you have completed all tasks, respond with FINAL ANSWER."
            )

        prompt = self._create_base_prompt()
        agent = create_react_agent(self.llm, [python_repl], prompt)
        return AgentExecutor(
            agent=agent, tools=[python_repl], verbose=True, handle_parsing_errors=True
        )

    def _create_base_prompt(self) -> PromptTemplate:
        instructions = """
        You are an agent that writes and executes python code
        You have access to a Python abstract REPL, which you can use to execute the python code.
        You must write the python code assuming that the dataframe (stored as df) has already been read.
        If you get an error, debug your code and try again.
        You might know the answer without running any code, but you should still run the code to get the answer.
        If it does not seem like you can write code to answer the question, just return "I don't know" as the answer.
        Do not create example dataframes
        """

        template = """
        {instructions_template}
        TOOLS:
        ------
        You have access to the following tools:
        {tools}
        To use a tool, please use the following format:
        ```
        Thought: Do I need to use a tool? Yes
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        ```
        When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:
        ```
        Thought: Do I need to use a tool? No
        Final Answer: \n Observation
        ```
        Begin!
        Previous conversation history:
        {chat_history}
        New input: {input}
        {agent_scratchpad}
        """

        base_prompt = PromptTemplate(
            template=template,
            input_variables=[
                "agent_scratchpad",
                "input",
                "instructions",
                "tool_names",
                "tools",
            ],
        )
        return base_prompt.partial(instructions_template=instructions)