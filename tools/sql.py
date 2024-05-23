import sqlite3
from langchain.tools import tool
from pydantic.v1 import BaseModel

conn = sqlite3.connect("db.sqlite")

def list_tables():
  c = conn.cursor()
  c.execute("SELECT name FROM sqlite_master WHERE type='table';")
  tables = c.fetchall()
  return tuple(item[0] for item in tables)


class RunQueryToolArgSchema(BaseModel):
  query: str


@tool(
  args_schema=RunQueryToolArgSchema
)
def run_query_tool(query):
  """
  Given a query string, run the query and return the result.
  """
  try:
    c = conn.cursor()
    c.execute(query)
    return c.fetchall()
  except Exception as e:
    return f"An exception occurred {str(e)}"
  
  
class DescribeTableSchema(BaseModel):
  tables: list[str]

@tool(
  args_schema=DescribeTableSchema,
)
def describe_tables_tool(tables: list[str]):
  """
  Given a list of table names, return SQL schema of these tables
  """
  sql_table_list = ', '.join([f"'{table}'" for table in tables])
  query = f"SELECT sql FROM sqlite_master WHERE type='table' AND name IN ({sql_table_list})"

  c = conn.cursor()
  rows = c.execute(query)
  return '\n'.join(row[0] for row in rows if row[0] is not None)
