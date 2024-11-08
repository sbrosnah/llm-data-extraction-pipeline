input_text_for_examples = """
The ocean is one of the most mysterious and captivating places on Earth. Covering more than 70% of the planet’s surface, it is home to an incredible 
diversity of life, from the smallest plankton to the largest mammals on Earth—blue whales. The ocean's depths hold uncharted ecosystems and stunning 
geological features, like underwater mountain ranges and vast trenches, some deeper than Mount Everest is tall. Despite its importance, much of the ocean 
remains unexplored, making it a frontier filled with unknown wonders and discoveries waiting to be uncovered. Ocean currents also play a crucial role in 
regulating the Earth's climate, distributing heat across the globe, which affects weather patterns, temperatures, and the sustainability of many ecosystems.

The ocean is not just a habitat for marine creatures, but also a vital resource for humanity. Millions of people around the world rely on the ocean for their 
livelihood, including those in the fishing, shipping, and tourism industries. It is also a source of inspiration for countless works of art, literature, 
and music, invoking feelings of adventure, tranquility, and respect for the natural world. However, human activity poses a serious threat to the health of 
our oceans. Pollution, overfishing, and climate change have resulted in the degradation of marine ecosystems and a loss of biodiversity. Addressing these 
challenges requires global cooperation and a shared commitment to preserving the ocean's beauty and bounty for future generations.
"""

ENTITY_EXTRACTION_EXAMPLES = [
    {
        "input": 
"""\
Text:
The ocean is one of the most mysterious and captivating places on Earth.
""",
        "output": 
"""\
<scratchpad>
Possible entities: 
    - "ocean" 
    - "Earth"
Possible types:
    - "ocean": GEOGRAPHICAL_FEATURE
    - "Earth": PLANET
</scratchpad>
[
   {"entity_name": "ocean", "entity_types": ["GEOGRAPHICAL_FEATURE"]},
   {"entity_name": "biodiversity", "entity_types": ["PLANET"]}
]
"""
    },
   {
      "input": 
"""\
Text:
Covering more than 70% of the planet's surface, it is home to an incredible diversity of life, from the smallest plankton to the largest mammals on Earth—blue whales.
""",
      "output": 
"""\
<scratchpad>
Possible entities:
   - "70%"
   - "planet's surface"
   - "plankton"
   - "blue whales"
   - "Earth"
Possible types:
   - "70%": PERCENTAGE
   - "planet's surface": GEOGRAPHICAL_FEATURE
   - "plankton": ORGANISM
   - "blue whales": ANIMAL, MAMMAL
   - "Earth": PLANET
</scratchpad>
[
   {"entity_name": "70%", "entity_types": ["PERCENTAGE"]},
   {"entity_name": "planet's surface", "entity_types": ["GEOGRAPHICAL_FEATURE"]},
   {"entity_name": "plankton", "entity_types": ["ORGANISM"]},
   {"entity_name": "blue whales", "entity_types": ["ANIMAL", "MAMMAL"]},
   {"entity_name": "Earth", "entity_types": ["PLANET"]}
]
"""
   },
   {
      "input": 
"""\
Text:
The ocean's depths hold uncharted ecosystems and stunning geological features, like underwater mountain ranges and vast trenches, some deeper than Mount Everest is tall.
""",
      "output": 
"""\
<scratchpad>
Possible entities: 
   - "ocean's depths" 
   - "ecosystems" 
   - "underwater mountain ranges" 
   - "trenches" 
   - "Mount Everest" 
Possible types: 
   - "ocean's depths": GEOGRAPHICAL_FEATURE 
   - "ecosystems": ENVIRONMENTAL_FEATURE 
   - "underwater mountain ranges": GEOGRAPHICAL_FEATURE 
   - "trenches": GEOGRAPHICAL_FEATURE 
   - "Mount Everest": MOUNTAIN, LOCATION
</scratchpad>
[
   {"entity_name": "ocean's depths", "entity_types": ["GEOGRAPHICAL_FEATURE"]},
   {"entity_name": "ecosystems", "entity_types": ["ENVIRONMENTAL_FEATURE"]},
   {"entity_name": "underwater mountain ranges", "entity_types": ["GEOGRAPHICAL_FEATURE"]},
   {"entity_name": "trenches", "entity_types": ["GEOGRAPHICAL_FEATURE"]},
   {"entity_name": "Mount Everest", "entity_types": ["MOUNTAIN", "LOCATION"]}
]
"""
   },
   {
      "input": 
"""\
Text:
Despite its importance, much of the ocean remains unexplored, making it a frontier filled with unknown wonders and discoveries waiting to be uncovered.
""",
      "output": 
"""\
<scratchpad>
Possible entities: 
   - "ocean"
   - "frontier"
   - "wonders"
   - "discoveries"
Possible types:
   - "ocean": GEOGRAPHICAL_FEATURE
   - "frontier": CONCEPT
   - "wonders": OBJECT, PHENOMENON
   - "discoveries": FINDING, INNOVATION, KNOWLEDGE
</scratchpad>
[
   {"entity_name": "ocean", "entity_types": ["GEOGRAPHICAL_FEATURE"]},
   {"entity_name": "frontier", "entity_types": ["CONCEPT"]},
   {"entity_name": "wonders", "entity_types": ["OBJECT", "PHENOMENON"]},
   {"entity_name": "discoveries", "entity_types": ["FINDING", "INNOVATION", "KNOWLEDGE"]}
]
"""
   },
   {
      "input": 
"""\
Text:
Ocean currents also play a crucial role in regulating the Earth's climate, distributing heat across the globe, which affects weather patterns, temperatures, and the sustainability of many ecosystems.
""",
      "output": 
"""\
<scratchpad>
Possible entities:
   - "ocean currents"
   - "Earth"s climate"
   - "heat"
   - "globe"
   - "weather patterns"
   - "temperatures"
   - "sustainability"
   - "ecosystems"
Possible types:
   - "ocean currents": NATURAL_PHENOMENON, OCEANOGRAPHIC_FEATURE
   - "Earth"s climate": CLIMATE
   - "heat": ENERGY, NATURAL_PHENOMENON
   - "globe": PLANET, LOCATION
   - "weather patterns": WEATHER_FEATURE, NATURAL_PHENOMENON
   - "temperatures": WEATHER_FEATURE, MEASUREMENT
   - "sustainability": CONCEPT, ENVIRONMENTAL_QUALITY
   - "ecosystems": ENVIRONMENTAL_FEATURE
</scratchpad>
[
   {"entity_name": "ocean currents", "entity_types": ["NATURAL_PHENOMENON", "OCEANOGRAPHIC_FEATURE"]},
   {"entity_name": "Earth"s climate", "entity_types": ["CLIMATE"]},
   {"entity_name": "heat", "entity_types": ["ENERGY", "NATURAL_PHENOMENON"]},
   {"entity_name": "globe", "entity_types": ["PLANET", "LOCATION"]},
   {"entity_name": "weather patterns", "entity_types": ["WEATHER_FEATURE", "NATURAL_PHENOMENON"]},
   {"entity_name": "temperatures", "entity_types": ["WEATHER_FEATURE", "MEASUREMENT"]},
   {"entity_name": "sustainability", "entity_types": ["CONCEPT", "ENVIRONMENTAL_QUALITY"]},
   {"entity_name": "ecosystems", "entity_types": ["ENVIRONMENTAL_FEATURE"]}
]
"""
   },
   {
      "input": 
"""\
Text:
The ocean is not just a habitat for marine creatures, but also a vital resource for humanity.
""",
      "output": 
"""\
<scratchpad>
Possible entities:
   - "ocean"
   - "marine creatures"
   - "humanity"
Possible types:
   - "ocean": GEOGRAPHICAL_FEATURE, RESOURCE, HABITAT
   - "marine creatures": BIOLOGICAL_ENTITY, FAUNA
   - "humanity": CONCEPT, SOCIAL_GROUP
</scratchpad>
[
   {"entity_name": "ocean", "entity_types": ["GEOGRAPHICAL_FEATURE", "RESOURCE", "HABITAT"]},
   {"entity_name": "marine creatures", "entity_types": ["BIOLOGICAL_ENTITY", "FAUNA"]},
   {"entity_name": "humanity", "entity_types": ["CONCEPT", "SOCIAL_GROUP"]}
]
"""
   },
   {
      "input": 
"""\
Text:
Millions of people around the world rely on the ocean for their livelihood, including those in the fishing, shipping, and tourism industries.
""",
      "output": 
"""\
<scratchpad>
Possible entities:
   - "Millions of people"
   - "ocean"
   - "fishing industry"
   - "shipping industry"
   - "tourism industry"
   - "livelihood"
Possible types:
   - "Millions of people": DEMOGRAPHIC_GROUP, POPULATION
   - "ocean": GEOGRAPHICAL_FEATURE, RESOURCE, HABITAT
   - "fishing industry": INDUSTRY
   - "shipping industry": INDUSTRY
   - "tourism industry": INDUSTRY
   - "livelihood": ECONOMIC_CONCEPT, SOCIAL_CONCEPT
</scratchpad>
[
   {"entity_name": "Millions of people", "entity_types": ["DEMOGRAPHIC_GROUP", "POPULATION"]},
   {"entity_name": "ocean", "entity_types": ["GEOGRAPHICAL_FEATURE", "RESOURCE", "HABITAT"]},
   {"entity_name": "fishing industry", "entity_types": ["INDUSTRY"]},
   {"entity_name": "shipping industry", "entity_types": ["INDUSTRY"]},
   {"entity_name": "tourism industry", "entity_types": ["INDUSTRY"]},
   {"entity_name": "livelihood", "entity_types": ["ECONOMIC_CONCEPT", "SOCIAL_CONCEPT"]}
]
"""
   },
      {
      "input": 
"""\
Text:
It is also a source of inspiration for countless works of art, literature, and music, invoking feelings of adventure, tranquility, and respect for the natural world.
""",
      "output": 
"""\
<scratchpad>
Possible entities:
   - "source of inspiration"
   - "art"
   - "literature"
   - "music"
   - "natural world"
Possible types:
   - "source of inspiration": HUMAN_CONCEPT
   - "art": CREATIVE_WORK
   - "literature": CREATIVE_WORK
   - "music": CREATIVE_WORK
   - "natural world": NATURAL_CONCEPT
</scratchpad>
[
   {"entity_name": "source of inspiration", "entity_types": ["HUMAN_CONCEPT"]},
   {"entity_name": "art", "entity_types": ["CREATIVE_WORK"]},
   {"entity_name": "literature", "entity_types": ["CREATIVE_WORK"]},
   {"entity_name": "music", "entity_types": ["CREATIVE_WORK"]},
   {"entity_name": "natural world", "entity_types": ["NATURAL_CONCEPT"]}
]
"""
   },
         {
      "input": 
"""\
Text:
However, human activity poses a serious threat to the health of our oceans.
""",
      "output": 
"""\
<scratchpad>
Possible entities:
   - "human activity"
   - "oceans"
   - "health"
   - "threat"
Possible types:
   - "human activity": HUMAN_ACTION, ANTHROPOGENIC_IMPACT
   - "oceans": GEOGRAPHICAL_FEATURE, ECOSYSTEM
   - "health": CONDITION, ENVIRONMENTAL_STATE
   - "threat": RISK, CONCEPT
</scratchpad>
[
   {"entity_name": "human activity", "entity_types": ["HUMAN_ACTION", "ANTHROPOGENIC_IMPACT"]},
   {"entity_name": "oceans", "entity_types": ["GEOGRAPHICAL_FEATURE", "ECOSYSTEM"]},
   {"entity_name": "health", "entity_types": ["CONDITION", "ENVIRONMENTAL_STATE"]},
   {"entity_name": "threat", "entity_types": ["RISK", "CONCEPT"]}
]
"""
   },
   {
      "input":
"""\
Text:
Pollution, overfishing, and climate change have resulted in the degradation of marine ecosystems and a loss of biodiversity.
""",
      "output":
"""\
<scratchpad>
Possible entities:
   - "Pollution"
   - "overfishing"
   - "climate change"
   - "marine ecosystems"
   - "biodiversity"
   - "loss of biodiversity"
   - "degradation of marine ecosystems"
Possible types:
   - "Pollution": ENVIRONMENTAL_ISSUE, ANTHROPOGENIC_IMPACT
   - "overfishing": ENVIRONMENTAL_ISSUE, ANTHROPOGENIC_IMPACT
   - "climate change": ENVIRONMENTAL_ISSUE, GLOBAL_PHENOMENON
   - "marine ecosystems": BIOLOGICAL_FEATURE, ECOSYSTEM, ENVIRONMENT
   - "biodiversity": BIOLOGICAL_CONCEPT, ECOLOGICAL_CONCEPT
   - "loss of biodiversity": ECOLOGICAL_IMPACT, BIOLOGICAL_CONCEPT
   - "degradation of marine ecosystems": ENVIRONMENTAL_IMPACT, ECOLOGICAL_IMPACT
</scratchpad>
[
   {"entity_name": "Pollution", "entity_types": ["ENVIRONMENTAL_ISSUE", "ANTHROPOGENIC_IMPACT"]},
   {"entity_name": "overfishing", "entity_types": ["ENVIRONMENTAL_ISSUE", "ANTHROPOGENIC_IMPACT"]},
   {"entity_name": "climate change", "entity_types": ["ENVIRONMENTAL_ISSUE", "GLOBAL_PHENOMENON"]},
   {"entity_name": "marine ecosystems", "entity_types": ["BIOLOGICAL_FEATURE", "ECOSYSTEM", "ENVIRONMENT"]},
   {"entity_name": "biodiversity", "entity_types": ["BIOLOGICAL_CONCEPT", "ECOLOGICAL_CONCEPT"]},
   {"entity_name": "loss of biodiversity", "entity_types": ["ECOLOGICAL_IMPACT", "BIOLOGICAL_CONCEPT"]},
   {"entity_name": "degradation of marine ecosystems", "entity_types": ["ENVIRONMENTAL_IMPACT", "ECOLOGICAL_IMPACT"]}
]
"""
   },
   {
      "input":
"""\
Text:
Addressing these challenges requires global cooperation and a shared commitment to preserving the ocean's beauty and bounty for future generations.
""",
      "output":
"""\
<scratchpad>
Possible entities:
   - "global cooperation"
   - "ocean's beauty"
   - "ocean's bounty"
   - "future generations"
Possible types:
   - "global cooperation": HUMAN_ENDEAVOR, SOCIAL_CONCEPT
   - "ocean's beauty": ENVIRONMENTAL_QUALITY, AESTHETIC_ASPECT
   - "ocean's bounty": NATURAL_RESOURCE, ECOLOGICAL_ASSET
   - "future generations": DEMOGRAPHIC_GROUP, SOCIAL_CONCEPT
</scratchpad>
[
   {"entity_name": "global cooperation", "entity_types": ["HUMAN_ENDEAVOR", "SOCIAL_CONCEPT"]},
   {"entity_name": "ocean's beauty", "entity_types": ["ENVIRONMENTAL_QUALITY", "AESTHETIC_ASPECT"]},
   {"entity_name": "ocean's bounty", "entity_types": ["NATURAL_RESOURCE", "ECOLOGICAL_ASSET"]},
   {"entity_name": "future generations", "entity_types": ["DEMOGRAPHIC_GROUP", "SOCIAL_CONCEPT"]}
]
"""
   }
]