import sqlite3
from langchain.tools import Tool

conn = sqlite3.connect("db.sqlite")

def run_sqlite_query(query):
  try:
    c = conn.cursor()
    c.execute(query)
    return c.fetchall()
  except Exception as e:
    return f"An exception occurred {str(e)}"

def list_tables():
  c = conn.cursor()
  c.execute("SELECT name FROM sqlite_master WHERE type='table';")
  tables = c.fetchall()
  return tuple(item[0] for item in tables)

def describe_tables(tables: list[str] | str):
  if isinstance(tables, list):
    sql_table_list = ', '.join([f"'{table}'" for table in tables])
  else:
    sql_table_list = f"'{tables}'"
    
  query = f"SELECT sql FROM sqlite_master WHERE type='table' AND name IN ({sql_table_list})"
  print(query)

  c = conn.cursor()
  rows = c.execute(query)
  return '\n'.join(row[0] for row in rows if row[0] is not None)


run_query_tool = Tool.from_function(
  name="run_sqlite_query",
  description="Given a query string, run the query and return the result.",
  func=run_sqlite_query
)

describe_tables_tool = Tool.from_function(
  name="describe_table_tool",
  description="Given a list of table names, return SQL schema of these tables",
  func=describe_tables
)
