from langchain.tools import StructuredTool
from pydantic.v1 import BaseModel

class ExportReportSchema(BaseModel):
  filename: str
  html: str


def export_report(filename: str, html: str):
  with open(filename, "w") as f:
    f.write(html)


export_report_tool = StructuredTool.from_function(
  name="export_report_tool",
  description="Given HTML content, write it to a local file. \n"
  "Use this tool when you already have the HTML content and need to write it to a local disk file.",
  func=export_report,
  args_schema=ExportReportSchema
)
