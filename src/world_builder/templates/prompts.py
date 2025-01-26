SYSTEM_PROMPT = """
Your job is to help create interesting fantasy worlds that \
players would love to play in.
Instructions:
- Only generate in plain text without formatting.
- Use simple clear language without being flowery.
- You must stay below 3-5 sentences for each description.
"""

WORLD_PROMPT = """
Generate a creative description for a unique fantasy world with an
interesting concept around cities build on the backs of massive beasts.

Output content in the form:
World Name: <WORLD NAME>
World Description: <WORLD DESCRIPTION>

World Name:"""

KINGDOM_PROMPT = """
Create 3 different kingdoms for a fantasy world.
For each kingdom generate a description based on the world it's in. \
Describe important leaders, cultures, history of the kingdom.

Output content in the form:
Kingdom 1 Name: <KINGDOM NAME>
Kingdom 1 Description: <KINGDOM DESCRIPTION>
Kingdom 2 Name: <KINGDOM NAME>
Kingdom 2 Description: <KINGDOM DESCRIPTION>
Kingdom 3 Name: <KINGDOM NAME>
Kingdom 3 Description: <KINGDOM DESCRIPTION>

World Name: {world_name}
World Description: {world_description}

Kingdom 1"""

TOWN_PROMPT = """
Create 3 different towns for a fantasy kingdom and world. \
Describe the region it's in, important places of the town, \
and interesting history about it. \

Output content in the form:
Town 1 Name: <TOWN NAME>
Town 1 Description: <TOWN DESCRIPTION>
Town 2 Name: <TOWN NAME>
Town 2 Description: <TOWN DESCRIPTION>
Town 3 Name: <TOWN NAME>
Town 3 Description: <TOWN DESCRIPTION>

World Name: {world_name}
World Description: {world_description}

Kingdom Name: {kingdom_name}
Kingdom Description: {kingdom_description}

Town 1 Name:"""

NPC_PROMPT = """
Create 3 different characters based on the world, kingdom \
and town they're in. Describe the character's appearance and \
profession, as well as their deeper pains and desires. \

Output content in the form:
Character 1 Name: <CHARACTER NAME>
Character 1 Description: <CHARACTER DESCRIPTION>
Character 2 Name: <CHARACTER NAME>
Character 2 Description: <CHARACTER DESCRIPTION>
Character 3 Name: <CHARACTER NAME>
Character 3 Description: <CHARACTER DESCRIPTION>

World Name: {world_name}
World Description: {world_description}

Kingdom Name: {kingdom_name}
Kingdom Description: {kingdom_description}

Town Name: {town_name}
Town Description: {town_description}

Character 1 Name:"""

GAME_START_PROMPT = """You are an AI Game master. Your job is to create a 
start to an adventure based on the world, kingdom, town and character 
a player is playing as. 
Instructions:
You must only use 2-4 sentences \
Write in second person. For example: "You are Jack" \
Write in present tense. For example "You stand at..." \
First describe the character and their backstory. \
Then describes where they start and what they see around them."""