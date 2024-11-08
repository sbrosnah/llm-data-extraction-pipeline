from entity_extraction.prompts.entity_extraction_prompts import *
from model import Message
from entity_extraction.entity_extraction_model import EntityExtractionResponse, Entity
from openai import OpenAI
import json

################### call_model ###########################

def call_openai_structured(client: OpenAI, messages: list[dict]) -> str:
            
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=messages,
        response_format=EntityExtractionResponse,
    )
    
    #TODO: fix this
    result = completion.choices[0].message.parsed.model_dump_json()
    return json.dumps(result, indent=4)

def call_openai_unstructured(client: OpenAI, messages: list[dict]) -> str:
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
        
    return completion.choices[0].message.content

################### handle_assistant_msg ###########################

def handle_assistant_msg_append(messages: list[dict], raw_result: str) -> None:
    messages.append(Message('assistant', raw_result).to_json())
    
def handle_assistant_msg_replace(messages: list[dict], raw_result: str) -> None:
    messages[-1] = Message('assistant', raw_result).to_json()

################### handle_user_msg ###########################

def handle_user_msg_append(messages: list[dict], input_message: str, error_message: str) -> None:
    if error_message is not None:
        input_message = error_message
    messages.append(Message('user', input_message).to_json())

def handle_user_msg_replace(messages: list[dict], input_message: str, error_message: str) -> None:
    messages[-1] = Message('user', input_message).to_json()
    

################### update_final_data_set ###########################
    
def update_final_entity_set_dynamic(result: dict, final_entity_set: set) -> None:
    #Delete old ones
    for e in result["entities_to_delete"]:
        #TODO: maybe use remove with an error and indicate if it wasn't found
        final_entity_set.discard(Entity(e))
    
    #Add all new ones 
    for e in result["new_and_updated_entities"]:
        final_entity_set.add(Entity(e))

def update_final_entity_set_aggregate(result: list, final_entity_set: dict[Entity, list[str]], text: str=None) -> None:
    #Add all new ones 
    for e in result:
        entity = Entity(e)
        if entity in final_entity_set and text is not None:
            final_entity_set[entity].append(text)
        
        final_entity_set[entity] = []

#################### end_early ##########################

def end_early_dynamic_entity_extraction(result: dict):
    return result is not None and len(result['new_and_updated_entities']) == 0 and len(result['entities_to_delete']) == 0

def end_early_aggregate_entity_extraction(result: dict):
    return len(result) == 0

#################### get_extraction_message ########################

def get_base_entity_extraction_msg(input_text: str, already_extracted_entities: dict, gleaning: int):
    return INPUT_TEMPLATE_ENTITY_EXTRACTION.format(input_text= input_text, 
                                    already_extracted_entities=already_extracted_entities)
    
def get_gleaning_entity_extraction_msg_w_text(input_text: str, already_extracted_entities: dict, gleaning: int):
    input_message = get_base_entity_extraction_msg(input_text, already_extracted_entities, gleaning)
    if gleaning > 0:
        input_message = GLEANING_TEMPLATE_ENTITY_EXTRACTION + "\n" + input_message
    return input_message

def get_gleaning_entity_extraction_msg_wo_text(input_text: str, already_extracted_entities: dict, gleaning: int):
    if gleaning == 0:
        input_message = get_base_entity_extraction_msg(input_text, already_extracted_entities, gleaning)
    else:
        input_message = GLEANING_TEMPLATE_ENTITY_EXTRACTION
    return input_message