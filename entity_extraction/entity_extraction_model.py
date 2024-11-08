from pydantic import BaseModel
from model import ExtractedDataObject, ExtractionStrategy

############### Strategy Specific Models #################

class ResponseEntity(BaseModel):
  entity_name: str
  entity_types: list[str]
  
class EntityExtractionResponse(BaseModel):
  new_and_updated_entities: list[ResponseEntity]
  entities_to_delete: list[ResponseEntity]
  
class Entity(ExtractedDataObject):
  def __init__(self, json):
    
    self._name: str = json["entity_name"]
    self._types: set[str] = set(json["entity_types"])
    
  def __eq__(self, other):
    if not isinstance(other, Entity):
      return NotImplemented
    
    return self._name == other._name and frozenset(self._types) == frozenset(other._types)
  
  def __hash__(self):
    return hash(self._name) + hash(frozenset(self._types))
  
  def to_json(self):
    return {"entity_name": self._name, "entity_types": list(self._types)}

#Set desired functions here by importing them from strategy_functions 
from strategy_functions import *

#Only use one of these for each output data type. Can chain them together 
class Strategy(ExtractionStrategy):
  def update_final_data_set(self, result: dict, final_entity_set: dict[Entity, list[str]], text:str=None) -> None:
    return update_final_entity_set_aggregate(result, final_entity_set, text)
  
  def get_extraction_message(self, input_text: str, final_entities: dict, gleaning: int) -> str:
    return get_gleaning_entity_extraction_msg_wo_text(input_text, final_entities, gleaning)
  
  def handle_user_msg(self, messages: list[dict], input_message: str, error_message: str) -> None:
    handle_user_msg_append(messages, input_message, error_message)

  def call_model(self, client: any, messages: list[dict]) -> str:
    return call_openai_unstructured(client, messages) 
  
  def handle_assistant_msg(self, messages: list[dict], raw_result: str) -> None:
    handle_assistant_msg_append(messages, raw_result)
  
  def end_early(self, result: dict) -> None:
    return end_early_aggregate_entity_extraction(result)
  
  def get_json_chars(self):
    return ("[", "]")