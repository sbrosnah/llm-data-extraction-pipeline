UPDATE_DELETE_ENTITY_GUIDELINES = {
    "VERBATIM_ENTITIES": {
      "instruction":
"""\
Verbatim Entities:

When entities are to be updated, add the VERBATIM old version of the entity to be updated to the list of entities to delete in the output and put the new (updated) version in the new entities list.
""",
      "example":
"""\
Text:
Bob, who likes cheese, is fat.

Already Extracted Entities:
[
  {"entity_name": "Bob", "entity_types": ["PERSON"]},
  {"entity_name": "cheese", "entity_types": ["OBJECT"]}
]

Output:
<scratchpad>[your reasoning about the entities in the text]</scratchpad>
{
  "new_and_updated_entities": [
    {"entity_name": "cheese", "entity_types": ["FOOD"]}
  ],
  "entities_to_delete": [
    {"entity_name": "cheese", "entity_types": ["OBJECT"]}
  ]
}
"""
    },
    "TYPE_CONSISTENCY": {
      "instruction":
"""\
Enforce Entity Type Consistency: 

If an entity in the list of entities already extracted shares the same type as an entity you are currently 
extracting, then only one should be chosen. If a new one is chosen and an entity in the list fits that new type, it's type should be updated or added to it's
type list. Remember, that a type list should not be repetitive and each type should represent something distinct. 
""",
      "example": 
"""\
Text:
The University of California, Berkeley and Cornell are major research universities.

Already Extracted Entities:
[
  {"entity_name": "The University of California, Berkeley", "entity_types": ["ORGANIZATION"]},
  {"entity_name": "Berkeley", "entity_types": ["LOCATION"]}
]

Output:
<scratchpad>[your reasoning about the entities in the text]</scratchpad>
{
  "new_and_updated_entities": [
    {"entity_name": "Cornell", "entity_types": ["UNIVERSITY"]},
    {"entity_name": "The University of California, Berkeley", "entity_types": ["UNIVERSITY"]}
  ],
  "entities_to_delete": [
    {"entity_name": "The University of California, Berkeley", "entity_types": ["ORGANIZATION"]}
  ]
}
"""
    },

  "NAME_COMPLETENESS": {
    "instruction":
"""\
Ensure Entity Name Completeness: 

If a more complete name is found for an already extracted entity, then it should be updated. For example, if you previously had the 
entity name "John" and you found out his full name is "John Doe", then the entity name should be updated to "John Doe". 
""",
    "example":
"""\
Text:
Elon musk, the CEO of Tesla, spoke at the conference. The conference was Comic Con

Already Extracted Entities:
[
  {"entity_name": "conference", "entity_types": ["EVENT"]},
  {"entity_name": "Elon Musk", "entity_types": ["CEO", "PERSON"]}
]

Output:
<scratchpad>[your reasoning about the entities in the text]</scratchpad>
{
  "new_and_updated_entities": [
    {"entity_name": "Comic Con", "entity_types": ["CONFERENCE", "EVENT"]}
  ],
  "entities_to_delete": [
    {"entity_name": "conference", "entity_types": ["EVENT"]}
  ]
}
"""
  },

  "CORRECTNESS": {
    "instruction":
"""\
Ensure Correctness: 

If something is incorrect in a previously extracted entity, fix it and add the new version to the updated entities list. If any of the these guidlines, or the ones in the previous section
are violated, it needs to be fixed. 
""",
    "example":
"""\
Text:
There was a man named John Doe.

Already Extracted Entities:
[
  {"entity_name": "John", "entity_types": ["ANIMAL"]},
  {"entity_name": "man", "entity_types": ["GENDER"]}
]

Output:
{
  "new_and_updated_entities": [
    {"entity_name": "John Doe", "entity_types": ["PERSON", "NAME"]}
  ],
  "entities_to_delete": [
    {"entity_name": "John Doe", "entity_types": ["ANIMAL"]}
  ]
}
"""
  },

  "REPETITIVENESS": {
    "instruction":
"""\
Reduce Repetitiveness:

No entities should be repeated. If two entities can be merged because they represent the same entity, then you should merge them. 
""",
    "example":
"""\
Example:

Text:
The capital of France is Paris. Paris is known for its Eiffel Tower.

Already Extracted Entities:
[
  {"entity_name": "Paris", "entity_types": ["CITY", "PLACE]},
  {"entity_name": "Paris", "entity_types": ["CITY"]},
]

Output:
{
  'new_and_updated_entities': [],
  'entities_to_delete': [
    {"entity_name": "Paris", "entity_types": ["CITY"]},
  ]
}

"""
  },
  "NECESSITY": {
    "instruction":
"""\
Only Update if Necessary:

Don't update or delete unless it's necessary.
""",
    "example": 
"""\
Text:
There was a man named John Doe.

Already Extracted Entities:
[
  {"entity_name": "John Doe", "entity_types": ["PERSON", "NAME"]},
]

Output:
{
  "new_and_updated_entities": [],
  "entities_to_delete": []
}
"""
  },
  "FORMATTING": {
    "instruction":
"""\
Enforce Proper Formatting:

Ensure that there is consistent formatting. If there is poor formatting in an already extracted entity, fix it.
""",
    "example": 
"""\
Text:
Elon musk, the CEO of Tesla, spoke at the conference.

Already Extracted Entities:
[
  {"entity_name": "elon musk", "entity_types": ["Person", "ceo"]},
  {"entity_name": "conference", "entity_types": ["event"]}
]

Output:
{
  "new_and_updated_entities": [
    {"entity_name": "Elon Musk", "entity_types": ["PERSON", "CEO"]},
    {"entity_name": "conference", "entity_types": ["EVENT"]}
  ],
  "entities_to_delete": [
    {"entity_name": "elon musk", "entity_types": ["Person", "ceo"]},
    {"entity_name": "conference", "entity_types": ["event"]}
  ]
}
"""
  }
}

SYSTEM_TEMPLATE_ENTITY_EXTRACTION_AND_UPDATE ="""\
You are an expert in constructing and editing knowledge graph nodes. Your current task is entities from the provided text to be used in a knowledge graph.

You will be given an input text and a list of already extracted entities.

Your task has two main parts:
1. Extracting new entities
2. Updating old entities (if needed)

----------------------------------------------------------------------

GUIDELINES FOR EXTRACTING ENTITIES:

{extraction_guidelines}

----------------------------------------------------------------------

GUIDELINES FOR UPDATING/DELETING ENTITIES

In general, you update the entities from the 'Already Extracted Entities' list so that they adhere to the guidelines given above. 
This section gives guidelines on how to perform these updates and gives specific cases for when to do so.

{update_delete_guidelines}

----------------------------------------------------------------------

To help with your task, follow the given steps and write them out between <scratchpad><\scratchpad> tags. WRITE EVERY THOUGHT YOU HAVE.

STEPS:
1. Analyze every sentence one at a time. You should write out every single sentence and list the following below.
  a. Take note of all possible entities in the sentence (even if they are already in the 'Already Extracted Entities' list)
  b. take not of all possible types for each entity
2. Create a list of all the unique entities found with your best guess for the types that should be assigned to each entity. Actually write it out.
3. Step through each of the entity extraction guidelines and refine the entity list as needed. Actually write out each guideline and take note of the entities that need to be updated below each guideline.
4. Write out the list of extracted entities after the updates
5. Now that you've extracted the entities from the text, compare it with the Already Extracted Entities. If there isn't one, skip this step.
  a. If two entities can be reasonably merged, do so
  b. If an entity is already in the Already Extracted Entity list, there is no need to include it in the new_and_updated_entities list. 
  c. If one of the newly extracted entities is more complete than an Already Extracted Entity, re
6. Output the final JSON object.

----------------------------------------------------------------------

IMPORTANT: The output outside of the <scratchpad><\scratchpad> tags must be in JSON format only!!! 

Output Format:
Provide the output (outside of the <scratchpad><\scratchpad> tags) in the following structured format:
{{
  "new_and_updated_entities": [
    {{"entity_name": "NewEntity1", "entity_types": ["Type1"]}},
    {{"entity_name": "NewEntity2", "entity_types": ["Type2"]}},
    ...
  ],
  "entities_to_delete": [
    {{"entity_name": "OldEntity1", "entity_types": ["Type1"]}},
    {{"entity_name": "OldEntity2", "entity_types": ["Type1", "Type2"]}},
    ...
  ]
}}
"""

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

def get_entity_extraction_and_update_system_prompt():
  return SYSTEM_TEMPLATE_ENTITY_EXTRACTION_AND_UPDATE.format(
    extraction_guidelines=get_guidelines(ENTITY_EXTRACTION_GUIDELINES),
    update_delete_guidelines=get_guidelines(UPDATE_DELETE_ENTITY_GUIDELINES)
  )

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







