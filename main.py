import sys
import os

from config.logging_config import setup_logging

def setup_paths():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    for child_dir in [d.path for d in os.scandir(base_dir) if os.path.dirname(d.path) != 'config' and d.is_dir()]:
        if child_dir not in sys.path:
            sys.path.append(child_dir)
        
def setup():
    setup_paths()
    setup_logging()

setup()

from extraction_module import Extractor
from entity_extraction.entity_extraction_model import Strategy
from model import ExtractorConfig
from openai import OpenAI
from utils import split_into_sentences_regex

from entity_extraction.prompts.entity_extraction_prompts import get_entity_extraction_only_prompt
from entity_extraction.examples.entity_extraction_examples import ENTITY_EXTRACTION_EXAMPLES



input_text = """\
The early hours of dawn hold a unique magic that seems to belong to a world only half awake. As the sun begins its slow ascent, the sky shifts from deep indigo 
to a warm gradient of pinks and oranges, casting a gentle light over the quiet landscape. Birds, the first to greet the morning, 
start their songs, creating a delicate symphony that gradually grows in volume. The air feels crisp, carrying with it the earthy scent of dew-covered 
grass and the faint fragrance of blooming flowers. There’s a sense of renewal in those hours, as if each day offers a fresh canvas, waiting to be filled 
with new stories, choices, and experiences.

For those who rise early, these moments offer a rare gift: time to reflect, to breathe, and to simply exist before the demands of the day begin. There's a 
quiet clarity that settles in the mind as the world slowly wakes up. The first light touches everything with a soft brilliance, highlighting the intricate 
details of leaves, spiderwebs, and even the cracks on old pavement. It’s a time to pause and appreciate the beauty in everyday simplicity, to savor the small 
wonders that often go unnoticed in the rush of daily life. In these fleeting moments, there's a connection to something timeless and grounding—a reminder that, 
amidst all of life’s chaos, there’s still beauty in the beginning of each new day.
"""

if __name__ == '__main__':

    config = ExtractorConfig(llm=OpenAI(), 
                            strategy=Strategy(),
                            task_name="entity_extraction",
                            num_gleanings=1, 
                            max_errors_per_call=3)
    extractor = Extractor(config)


    sentences = split_into_sentences_regex(input_text)

    result = extractor.extract_data(inputs=sentences, 
                                document_id=str(0), 
                                system_prompt=get_entity_extraction_only_prompt(), 
                                examples=ENTITY_EXTRACTION_EXAMPLES[:5], 
                                input_data=[])

    print(result)
