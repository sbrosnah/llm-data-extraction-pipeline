import json
from model import Message, ExtractorConfig, ExtractedDataObject
import logging
import os
from utils import extract_json_string

logger = None

def setup_logging(logger_name):
    global logger
    logger = logging.getLogger(logger_name)

'''
Responsible for orchestrating the data extraction
- debug logging
- managing final data set while performing gleanings
- saving data
- error handling and sending errors to llm
- messaging the llm
Logic for individual strategies should be kept in the strategy objects
'''
class Extractor:
    def __init__(self, 
                 config: ExtractorConfig):
        
        self.client = config.llm
        self.strategy = config.strategy
        self.num_gleanings = config.num_gleanings
        self.max_errors_per_call = config.max_errors_per_call
        self.task_name = config.task_name
        setup_logging(config.task_name)
        
        self.messages = []
        self.output_trace = []
        self.already_extracted_data = []
        self.final_data: dict[ExtractedDataObject, list[str]] = {}

    def log_message(self):
        m = json.dumps(self.messages[-1], indent=4)
        m = m.replace("\\n", "\n")
        m = m.replace("\\\"", "\'")
        logger.info("message:\n{}".format(m))
        
    def perform_extraction(self, input_message):
        error_count = 0
        done = False
        error_msg = None
        while not done:
            try:
                self.strategy.handle_user_msg(self.messages, input_message, error_msg)
                    
                self.log_message()
                
                raw_result = self.strategy.call_model(self.client, self.messages)
                    
                self.strategy.handle_assistant_msg(self.messages, raw_result)
                    
                self.log_message()
                
                result = extract_json_string(raw_result, self.strategy.get_json_chars())

                if result == None:
                    raise Exception("Unable to extract JSON due to bad formatting in response. Please try again.")
                
                # Convert String to JSON
                result = json.loads(result)
                
                self.output_trace.append(result)
                    
                done = True
                
                return result
                
            except Exception as e:
                error_count += 1
                logger.error("Error in LLM. Retrying...")
                logger.error(e)
                error_msg = e.args[0]

                if error_count >= self.max_errors_per_call:
                    done = True
                    logger.error("Exceeded maximum retries. Exiting current prompt.")
    
    def save_data(self, output, document_id):
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        with open(os.path.join(base_dir, self.task_name, "results", f"output-trace-{document_id}.json"), "w", encoding='utf-8') as f:
            json.dump(self.output_trace, f)

        with open(os.path.join(base_dir, self.task_name, "results", f"output-{document_id}.json"), "w", encoding='utf-8') as f:
            json.dump(output, f)
    
    def get_already_extracted_data(self):
        return [e.to_json() for e in self.final_data]
    
    def get_already_extracted_data_str(self):
        return json.dumps([e.to_json() for e in self.final_data], indent=4)
                    
    def extract_data(self, inputs: list[str], document_id: str, system_prompt:str, examples: list[str], input_data:list = None) -> dict:
        logger.info(f"==================================EXTRACTING DATA FROM DOCUMENT {document_id}================================")
        
        self.messages = []
        self.final_data.clear()

        self.messages.append(Message("system", system_prompt).to_json())
        self.log_message()

        for e in examples:
            self.messages.append(Message("user", e["input"]).to_json())
            self.log_message()
            self.messages.append(Message("assistant", e["output"]).to_json())
            self.log_message()
        
        for j, input_text in enumerate(inputs):
            logger.info("on part: {j}")
        
            for i in range(self.num_gleanings):
                logger.info(f"on gleaning: {i}")
                input_message = self.strategy.get_extraction_message(input_text, self.get_already_extracted_data_str(), i)
                    
                result = self.perform_extraction(input_message)
                
                if result is not None:
                    self.strategy.update_final_data_set(result, self.final_data, input_text)
                
                if self.strategy.end_early(result):
                    logger.info("Breaking Early")
                    break
        
            output = self.get_already_extracted_data()
            
            self.save_data(output, f"{document_id}-{j}")
        
        logger.info(f"==================================FINISHED EXTRACTING DATA FROM DOCUMENT {document_id}================================")
        
        return output
        
    