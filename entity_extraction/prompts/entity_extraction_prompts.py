ENTITY_EXTRACTION_GUIDELINES = {
  "TYPE_SELECTION": {
    "instruction": 
"""\
Type Selection:

Examples of entity types are: PERSON, ORGANIZATION, LOCATION, DATE, TIME, MONEY, PERCENTAGE, EMAIL_ADDRESS, GEOGRAPHICAL_FEATURE etc.
The types chosen are not limited to this list. 
Entity types chosen should be consistent. For example, don't use ORGANIZATION if you've already used COMPANY and COMPANY applies to the entity. 
The entity types should be all upper-case with words separated by underscores ('_'). 
""",
    "example":
"""\
Text:
My favorite brand is Apple. It is a great company.

Output:
<scratchpad>[your reasoning about the entities in the text]</scratchpad>
[
  {"entity_name": "Apple", "entity_types": ["COMPANY", "BRAND"]},
]
""",
    "summary":
"""\
Types should be consistent and in the correct format. 
"""
  },
  
  "SINGULAR_ENTITIES": {
    "instruction":
"""\
Combine Types for Singular Entities

Each entity/list pair should only be represented once in the output. 
If an entity has multiple types, list them in a single list of strings assigned to the same entity, avoiding redundancy.
""",
    "example":
"""\
Text:
Steve Jobs is a person. He is also a CEO.

Output:
<scratchpad>[your reasoning about the entities in the text]</scratchpad>
[
  {"entity_name": "Steve Jobs", "entity_types": ["PERSON", "CEO"]},
]
""",
    "summary":
"""\
Entities should be unique and, if there are multiple types, they should be combined into a list in a singular entity.
"""
  }, #TODO: Maybe move this to update guidelines
#   "AMBIGIOUS_ENTITIES": {
#     "instruction": 
# """\
# Handling Ambiguous Entities: 

# Only extract entities if there is sufficient context to determine a reasonable entity/type combination. If the entity is 
# ambiguous, such as a pronoun without a clear referent, do not extract it. Entities are determined solely by the context of the text, not by the 
# reader's prior knowledge.

# For example: "They announced a new product." → Do not extract "They" since the referent is unclear.
# Or to see it in the expected format, refer to the example below. 
# """,
#     "example":
# """\
# Text:
# They announced a new product.

# Already Extracted Entities:
# []

# Output:
# <scratchpad>[your reasoning about the entities in the text]</scratchpad>
# {
#   "new_and_updated_entities": [],
#   "entities_to_delete": []
# }
# """
#   },
#   "AMBIGIOUS_ENTITIES": {
#     "instruction": 
# """\
# Handling Ambiguous Entities: 

# Only extract entities if there is sufficient context to determine a reasonable entity/type combination. If the entity is 
# ambiguous, such as a pronoun without a clear referent, do not extract it. Entities are determined solely by the context of the text, not by the 
# reader's prior knowledge.

# For example: "They announced a new product." → Do not extract "They" since the referent is unclear.
# Or to see it in the expected format, refer to the example below. 
# """,
#     "example":
# """\
# Text:
# They announced a new product.

# Output:
# <scratchpad>[your reasoning about the entities in the text]</scratchpad>
# []
# """
#   },
  "NESTED_ENTITIES": {
    "instruction": 
"""\
Handling Nested Entities: 

Prefer extracting the most specific entity when applicable. If there is a broader entity that can be reasonably extracted 
separately, extract both and indicate the relationship later.
""",
    "example":
"""\
Text:
The University of California, Berkeley is a major research university.

Output:
<scratchpad>[your reasoning about the entities in the text]</scratchpad>
[
  {"entity_name": "The University of California, Berkeley", "entity_types": ["ORGANIZATION", "UNIVERSITY", "RESEARCH_INSTITUTION"]},
  {"entity_name": "Berkeley", "entity_types": ["LOCATION"]}
]
""",
    "summary":
"""\
If entities are nested, entities at all levels should be extracted. However, entities should still be simple.
"""
  },
  "QUANTITIES": {
    "instruction": 
"""\
Extracting Quantities, Percentages, and Similar Measures:

Identify and extract numerical quantities, percentages, and other units of measurement from the text. 
When extracting such entities, ensure that the relevant unit or context is also captured (e.g., "20%", "5 kilometers", "12 dollars", "75 degrees Celsius"). 
Assign these entities appropriate types such as QUANTITY, PERCENTAGE, TEMPERATURE, CURRENCY, DISTANCE, etc., depending on the context provided in the text.
""",
    "example":
"""\
Text:
The company's revenue increased by 15% this quarter to reach $2 million.

Output:
<scratchpad>[your reasoning about the entities in the text]</scratchpad>
[
  {"entity_name": "15%", "entity_types": ["PERCENTAGE"]},
  {"entity_name": "company", "entity_types": ["ORGANIZATION"]},
  {"entity_name": "revenue", "entity_types": ["ECONOMIC_MEASURE"]},
  {"entity_name": "this quarter", "entity_types": ["TIME_PERIOD"]},
  {"entity_name": "$2 million", "entity_types": ["CURRENCY", "AMOUNT"]}
]
""",
    "summary":
"""\
Extract quantities and measurements. 
"""
  },

  "MULTI_WORD_ENTITIES":{
    "instruction": 
"""\
Handling Multi-Word Entities: 

Extract entities in their simplest form. When an entity can be further broken down, extract the simple components separately.
""",
    "example": 
"""\
Text:
Prime Minister Boris Johnson announced new policies.

Output:
<scratchpad>[your reasoning about the entities in the text]</scratchpad>
[
  {"entity_name": "Boris Johnson", "entity_types": ["PERSON"]},
  {"entity_name": "Prime Minister", "entity_types": ["ROLE"]},
  {"entity_name": "new policies", "entity_types": ["POLICY"]}
]
""",
    "summary":
"""\
Break down entities as much as possible.
"""
  },

  "COMPOUND_ENTITIES": {
    "instruction":
"""\
Handling Compound Entities: 

For compound entities, extract each individual component as a separate entity, not as a combined unit.
""",
    "example":
"""\
Text:
The United States and Canada signed a treaty.

Output:
<scratchpad>[your reasoning about the entities in the text]</scratchpad>
[
  {"entity_name": "The United States", "entity_types": ["LOCATION"]},
  {"entity_name": "Canada", "entity_types": ["LOCATION"]},
  {"entity_name": "treaty", "entity_types": ["DOCUMENT"]} 
]
""",
    "summary":
"""\
Separate compound entities.
"""
  },

  "TEMPORAL_EXPRESSIONS": {
    "instruction":
"""\
Handling Temporal Expressions: 

Extract temporal expressions in their entirety, even if they are descriptive or represent a range.
""",
    "example":
"""\
Text:
The city park project was started in the early 1990s and will end within the next two months.

Output:
<scratchpad>[your reasoning about the entities in the text]</scratchpad>
[
  {"entity_name": "city park project", "entity_types": ["PROJECT"]},
  {"entity_name": "early 1990s", "entity_types": ["DATE"]},
  {"entity_name": "the next two months", "entity_types": ["DURATION"]}
]
""",
    "summary":
"""\
Extract temporal expressions in their entirety.
"""
  },

  "PRONOUNS_AND_ACRONYMS":{
    "instruction":
"""\
Handling Pronouns and Acronyms: 

If the text provides sufficient context for acronyms or pronouns, extract them accordingly. 
If no clear referent can be identified, do not extract.
If the acronym or pronoun is unclear (e.g., "It" with no clear reference), it should not be extracted.
""",
    "example":
"""\
Text:
NASA launched a new satellite. It was their most advanced yet.

Output:
<scratchpad>[your reasoning about the entities in the text]</scratchpad>
[
  {"entity_name": "NASA", "entity_types": ["ORGANIZATION"]},
  {"entity_name": "new satellite", "entity_types": ["OBJECT"]}
]
""",
    "summary":
"""\
Perform coreference resolution to avoid extracting references without a referent.
"""
  },

  "AVOID_ADJECTIVES": {
    "instruction":
"""\
Avoid Adjectives in Entity Names: 

Do not include adjectives as part of the entity name or type. Adjectives should be considered attributes that are added later.
""",
    "example":
"""\
Text:
The famous inventor Nikola Tesla created numerous groundbreaking inventions.

Output:
<scratchpad>[your reasoning about the entities in the text]</scratchpad>
[
  {"entity_name": "Nikola Tesla", "entity_types": ["PERSON", "INVENTOR"]},
  {"entity_name": "inventions", "entity_types": ["CREATIVE_WORK", "INNOVATION"]}
]
""",
    "summary":
"""\
DON'T INCLUDE ADJECTIVES IN THE ENTITY NAMES! Entity names should be as simple as possible. 
"""
  }
}
  

SYSTEM_TEMPLATE_ENTITY_EXTRACTION_ONLY ="""\
You are an expert in constructing and editing knowledge graph nodes. Your current task is to extract entities from the provided text to be used in a knowledge graph.

----------------------------------------------------------------------

GUIDELINES FOR EXTRACTING ENTITIES:

{extraction_guidelines}

In summary, 
{guideline_summary}

----------------------------------------------------------------------

To help with your task, follow the given steps and write them out between <scratchpad><\scratchpad> tags. WRITE EVERY THOUGHT YOU HAVE.

STEPS:
1. Take note of all possible entities in the sentence
2. Take note of all possible types for each entity
3. Output the final JSON object.

----------------------------------------------------------------------

IMPORTANT: The output outside of the <scratchpad><\scratchpad> tags must be in JSON format only!!! 

Output Format:
Provide the output (outside of the <scratchpad><\scratchpad> tags) in the following structured format:
[
  {{"entity_name": "NewEntity1", "entity_types": ["Type1"]}},
  {{"entity_name": "NewEntity2", "entity_types": ["Type2", "Type3"]}},
  ...
]
"""


section_split = "="*70

def get_guidelines(guidelines):
  
  t = []
  
  for i, k in enumerate(guidelines.keys()):
    guideline = guidelines[k]
    instruction = str(i + 1) + ". " + guideline['instruction']
    components = [instruction, section_split + "\n"]
    example = guideline['example']
    if example is not None:
      components += ["Example:\n", example, section_split + "\n"]
    
    t.append("\n".join(components))
  
  return "\n".join(t)

def get_guideline_summary(guidelines):
  t = []
  
  for i, k in enumerate(guidelines.keys()):
    guideline = guidelines[k]
    summary = guideline['summary']
    t.append(str(i + 1) + ". " + summary)
  
  return "\n".join(t)

def get_entity_extraction_only_prompt():
  return SYSTEM_TEMPLATE_ENTITY_EXTRACTION_ONLY.format(
    extraction_guidelines=get_guidelines(ENTITY_EXTRACTION_GUIDELINES),
    guideline_summary=get_guideline_summary(ENTITY_EXTRACTION_GUIDELINES)
  )

INPUT_TEMPLATE_ENTITY_EXTRACTION = """\
Text:
{input_text}
"""

#TODO: Give a summary of the guidelines and ask for any updates to the entities
GLEANING_TEMPLATE_ENTITY_EXTRACTION = """\
Are you missing any entities or types?
Please output any new entities following the same instructions as before. If the previous list is complete, output an empty list.
"""







