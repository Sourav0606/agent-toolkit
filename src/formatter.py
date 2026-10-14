class TextFormatter:
  def __init__(self, prefix: str = ""):
    self.prefix = prefix

  def format_title(self, title: str) -> str:
    # Notice: 2-space indentation style used across this file!
    # Bug: strips leading spaces but forgets to capitalize words
    cleaned = title.strip()
    return f"{self.prefix}{cleaned}"
