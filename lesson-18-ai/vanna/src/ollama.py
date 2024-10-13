import json
import re

from httpx import Timeout

from ..base import VannaBase
from ..exceptions import DependencyError

from ..utils import LogTag

OFF_FLAG = True

class Ollama(VannaBase):
  def __init__(self, config=None):

    try:
      ollama = __import__("ollama")
    except ImportError:
      raise DependencyError(
        "You need to install required dependencies to execute this method, run command:"
        " \npip install ollama"
      )

    if not config:
      raise ValueError("config must contain at least Ollama model")
    if 'model' not in config.keys():
      raise ValueError("config must contain at least Ollama model")
    self.host = config.get("ollama_host", "http://localhost:11434")
    self.model = config["model"]
    if ":" not in self.model:
      self.model += ":latest"

    self.ollama_client = ollama.Client(self.host, timeout=Timeout(240.0))
    self.keep_alive = config.get('keep_alive', None)
    self.ollama_options = config.get('options', {})
    self.num_ctx = self.ollama_options.get('num_ctx', 2048)
    self.__pull_model_if_ne(self.ollama_client, self.model)

  @staticmethod
  def __pull_model_if_ne(ollama_client, model):
    model_response = ollama_client.list()
    model_lists = [model_element['model'] for model_element in
                   model_response.get('models', [])]
    if model not in model_lists:
      ollama_client.pull(model)

  def system_message(self, message: str) -> any:
    return {"role": "system", "content": message}

  def user_message(self, message: str) -> any:
    return {"role": "user", "content": message}

  def assistant_message(self, message: str) -> any:
    return {"role": "assistant", "content": message}

  def extract_sql(self, llm_response):
    """
    Extracts the first SQL statement after the word 'select', ignoring case,
    matches until the first semicolon, three backticks, or the end of the string,
    and removes three backticks if they exist in the extracted string.

    Args:
    - llm_response (str): The string to search within for an SQL statement.

    Returns:
    - str: The first SQL statement found, with three backticks removed, or an empty string if no match is found.
    """
    # Remove ollama-generated extra characters
    llm_response = llm_response.replace("\\_", "_")
    llm_response = llm_response.replace("\\", "")

    # Regular expression to find ```sql' and capture until '```'
    sql = re.search(r"```sql\n((.|\n)*?)(?=;|\[|```)", llm_response, re.DOTALL)
    # Regular expression to find 'select, with (ignoring case) and capture until ';', [ (this happens in case of mistral) or end of string
    select_with = re.search(r'(select|(with.*?as \())(.*?)(?=;|\[|```)',
                            llm_response,
                            re.IGNORECASE | re.DOTALL)
    self.log(title=LogTag.OUTPUT_LLM, message=llm_response, off_flag=OFF_FLAG)
    if sql:
      sql_stmt = sql.group(1).replace("```", "")
      self.log(title=LogTag.EXTRACTED_SQL, message=sql_stmt)
      return sql_stmt
    elif select_with:
      sql_stmt = select_with.group(0)
      self.log(title=LogTag.EXTRACTED_SQL, message=sql_stmt)
      return sql_stmt
    else:
      return llm_response

  def submit_prompt(self, prompt, **kwargs) -> str:
    msg = f"""
      model={self.model} ,
      options={self.ollama_options} ,
      keep_alive={self.keep_alive}
    """
    self.log(title=LogTag.OLLAMA_PARAMETERS, message=msg)
    self.log(title=LogTag.OLLAMA_PROMPT, message=json.dumps(prompt), off_flag=OFF_FLAG)
    response_dict = self.ollama_client.chat(model=self.model,
                                            messages=prompt,
                                            stream=False,
                                            options=self.ollama_options,
                                            keep_alive=self.keep_alive)
    self.log(title=LogTag.OLLAMA_RESPONSE, message=str(response_dict), off_flag=OFF_FLAG)

    return response_dict['message']['content']
