from abc import ABC, abstractmethod

class Message:
  role: str
  content: str 
  
  def __init__(self, role=None, content=None):
    self.role = role
    self.content = content 
  
  def to_json(self):
    return {"role": self.role, "content": self.content}

class ExtractionStrategy(ABC):
  @abstractmethod
  def update_final_data_set(self, result: any, final_entity_set: dict[any, list[str]], text: str=None) -> None:
    pass
  
  @abstractmethod
  def end_early(result: any) -> None:
    pass
  
  @abstractmethod
  def get_extraction_message(self, input_text: str, final_entities: dict, gleaning: int) -> str:
    pass
  
  @abstractmethod
  def handle_user_msg(self, messages: list[dict], input_message: str, error_message: str) -> None:
    pass
  
  @abstractmethod
  def call_model(self, client: any, messages: list[dict]) -> str:
    pass 
  
  @abstractmethod
  def handle_assistant_msg(self, messages: list[dict], raw_result: str) -> None:
    pass
  
  @abstractmethod
  def get_json_chars(self):
    pass
    

class ExtractorConfig():
  def __init__(self, 
               llm:any,
               strategy:ExtractionStrategy,
               task_name:str=None,
               num_gleanings:int = 5,
               max_errors_per_call:int = 3):
    
    self._llm = llm
    self._strategy = strategy
    self._task_name = task_name
    self._num_gleanings = num_gleanings
    self._max_errors_per_call = max_errors_per_call
  
  @property
  def llm(self):
    return self._llm
  
  @property
  def strategy(self):
    return self._strategy
  
  @property
  def task_name(self):
    return self._task_name

  @property
  def num_gleanings(self):
    return self._num_gleanings

  @property
  def max_errors_per_call(self):
    return self._max_errors_per_call

class ExtractedDataObject(ABC):
  @abstractmethod
  def to_json(self):
    pass
  

