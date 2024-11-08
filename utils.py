import re

def extract_json_string(output, c):

    output = remove_scratchpad_content(output)

    start = output.find(c[0])
    end = output.rfind(c[1])
    
    # Check if both '{' and '}' are present in the string
    if start != -1 and end != -1 and start < end:
        return output[start:end + 1]
    
    # Return an empty string if the substring cannot be extracted
    return None

def remove_scratchpad_content(text):
    # Use a regex pattern to match the content between <scratchpad> and </scratchpad>
    result = re.sub(r'<scratchpad>.*?</scratchpad>', '', text, flags=re.DOTALL)
    return result

def split_into_sentences_regex(paragraph):
    # Regular expression pattern
    sentence_endings = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s'
    sentences = re.split(sentence_endings, paragraph) 
    sentences = [sentence.replace('\n', '').strip() for sentence in sentences] 
    sentences = [s for s in sentences if len(s) > 0]
    return sentences    