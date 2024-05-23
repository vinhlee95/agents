from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
  ChatPromptTemplate,
  HumanMessagePromptTemplate,
  MessagesPlaceholder,
)
from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from tools.sql import list_tables, run_query_tool, describe_tables_tool
from dotenv import load_dotenv

load_dotenv()

import langchain
langchain.debug = True

llm = ChatOpenAI()

tables = list_tables()

prompt = ChatPromptTemplate(
  messages=[
    SystemMessage(content=
      f"You are an AI having access to a SQLite database having following tables: {tables}. \n"
      "Do not make any assumption about the tables. \n"
      "Instead always try to use 'describe_tables_tool' to get schema of relevant tables \n"
      "before you try to figure out the query."
    ),
    HumanMessagePromptTemplate.from_template("{input}"),
    # agent_scratchpad is specific, kinda a simple form of memorising 
    # the output of the tool in the chain
    MessagesPlaceholder(variable_name="agent_scratchpad")
  ],
  input_variables=[],
)

tools = [run_query_tool, describe_tables_tool]

agent = OpenAIFunctionsAgent(
  llm=llm,
  tools=tools,
  prompt=prompt,
)

agent_executor = AgentExecutor(
  agent=agent,
  tools=tools,
  verbose=True
)

agent_executor.run("How many users are in the database having non-empty shipping address?")