# src/world_builder/generator.py

from src.utils.helper import save_world,load_world
from .templates.prompts import (
    SYSTEM_PROMPT, 
    WORLD_PROMPT, 
    KINGDOM_PROMPT,
    TOWN_PROMPT,
    NPC_PROMPT
)

class WorldGenerator:
    def __init__(self, client):
        self.client = client
        self.world = None

    def generate_world(self):
        """Generate the initial world"""
        output = self.client.chat.completions.create(
            model="meta-llama/Llama-3-70b-chat-hf",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": WORLD_PROMPT}
            ],
        )
        
        world_output = output.choices[0].message.content.strip()
        self.world = {
            "name": world_output.split('\n')[0].strip().replace('World Name: ', ''),
            "description": '\n'.join(world_output.split('\n')[1:])
                .replace('World Description:', '').strip()
        }
        return self.world

    def generate_kingdoms(self):
        """Generate kingdoms for the world"""
        if not self.world:
            raise ValueError("Must generate world first")

        kingdom_prompt = KINGDOM_PROMPT.format(
            world_name=self.world['name'],
            world_description=self.world['description']
        )

        output = self.client.chat.completions.create(
            model="meta-llama/Llama-3-70b-chat-hf",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": kingdom_prompt}
            ],
        )

        kingdoms = {}
        kingdoms_output = output.choices[0].message.content

        for output in kingdoms_output.split('\n\n'):
            kingdom_name = output.strip().split('\n')[0].split('Name: ')[1].strip()
            kingdom_description = output.strip().split('\n')[1].split('Description: ')[1].strip()
            
            kingdom = {
                "name": kingdom_name,
                "description": kingdom_description,
                "world": self.world['name']
            }
            kingdoms[kingdom_name] = kingdom
            print(f'Created kingdom "{kingdom_name}" in {self.world["name"]}')

        self.world['kingdoms'] = kingdoms
        return kingdoms

    def generate_towns(self, kingdom):
        """Generate towns for a kingdom"""
        print(f'\nCreating towns for kingdom: {kingdom["name"]}...')
        
        town_prompt = TOWN_PROMPT.format(
            world_name=self.world['name'],
            world_description=self.world['description'],
            kingdom_name=kingdom['name'],
            kingdom_description=kingdom['description']
        )
        
        output = self.client.chat.completions.create(
            model="meta-llama/Llama-3-70b-chat-hf",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": town_prompt}
            ],
        )
        
        towns = {}
        towns_output = output.choices[0].message.content
        
        for output in towns_output.split('\n\n'):
            town_name = output.strip().split('\n')[0].split('Name: ')[1].strip()
            town_description = output.strip().split('\n')[1].split('Description: ')[1].strip()
            
            town = {
                "name": town_name,
                "description": town_description,
                "world": self.world['name'],
                "kingdom": kingdom['name']
            }
            towns[town_name] = town
            print(f'- {town_name} created')
            
        kingdom["towns"] = towns
        return towns

    def generate_npcs(self, kingdom, town):
        """Generate NPCs for a town"""
        print(f'\nCreating characters for the town of: {town["name"]}...')
        
        npc_prompt = NPC_PROMPT.format(
            world_name=self.world['name'],
            world_description=self.world['description'],
            kingdom_name=kingdom['name'],
            kingdom_description=kingdom['description'],
            town_name=town['name'],
            town_description=town['description']
        )
        
        output = self.client.chat.completions.create(
            model="meta-llama/Llama-3-70b-chat-hf",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": npc_prompt}
            ],
            temperature=1
        )

        npcs = {}
        npcs_output = output.choices[0].message.content
        
        for output in npcs_output.split('\n\n'):
            npc_name = output.strip().split('\n')[0].split('Name: ')[1].strip()
            npc_description = output.strip().split('\n')[1].split('Description: ')[1].strip()
            
            npc = {
                "name": npc_name,
                "description": npc_description,
                "world": self.world['name'],
                "kingdom": kingdom['name'],
                "town": town['name']
            }
            npcs[npc_name] = npc
            print(f'- "{npc_name}" created')
            
        town["npcs"] = npcs
        return npcs

    def _get_town_prompt(self, kingdom):
        """Generate town prompt"""
        return f"""
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
        
        World Name: {self.world['name']}
        World Description: {self.world['description']}
        
        Kingdom Name: {kingdom['name']}
        Kingdom Description: {kingdom['description']}
        
        Town 1 Name:"""

    def _get_npc_prompt(self, kingdom, town):
        """Generate NPC prompt"""
        return f"""
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
        
        World Name: {self.world['name']}
        World Description: {self.world['description']}
        
        Kingdom Name: {kingdom['name']}
        Kingdom Description: {kingdom['description']}
        
        Town Name: {town['name']}
        Town Description: {town['description']}
        
        Character 1 Name:"""

    def generate_complete_world(self):
        """Generate complete world with kingdoms, towns, and NPCs"""
        self.generate_world()
        self.generate_kingdoms()
        
        for kingdom in self.world['kingdoms'].values():
            self.generate_towns(kingdom)
            for town in kingdom['towns'].values():
                self.generate_npcs(kingdom, town)
        
        return self.world

    def save_world(self, filename):
        """Save the generated world to a file"""
        if not self.world:
            raise ValueError("No world generated yet")
        save_world(self.world, filename)  # Use the helper function

    def load_world(self, filename):
        """Load a previously generated world"""
        self.world = load_world(filename)  # Use the helper function
        return self.world
    
    def generate_game_start(self, kingdom_name=None, town_name=None, character_name=None):
        """Generate the game start description"""
        if not self.world:
            raise ValueError("Must generate world first")
            
        # If not specified, use first kingdom, town, and character
        if not kingdom_name:
            kingdom_name = list(self.world['kingdoms'].keys())[0]
        if not town_name:
            town_name = list(self.world['kingdoms'][kingdom_name]['towns'].keys())[0]
        if not character_name:
            town = self.world['kingdoms'][kingdom_name]['towns'][town_name]
            character_name = list(town['npcs'].keys())[0]

        # Get the required objects
        kingdom = self.world['kingdoms'][kingdom_name]
        town = kingdom['towns'][town_name]
        character = town['npcs'][character_name]

        # Create world info
        world_info = f"""
        World: {self.world['description']}
        Kingdom: {kingdom['description']}
        Town: {town['description']}
        Your Character: {character['description']}
        """

        # Generate start
        output = self.client.chat.completions.create(
            model="meta-llama/Llama-3-70b-chat-hf",
            temperature=1.0,
            messages=[
                {"role": "system", "content": GAME_START_PROMPT},
                {"role": "user", "content": world_info + '\nYour Start:'}
            ],
            max_tokens=1800
        )

        # Add start to world
        self.world['start'] = output.choices[0].message.content
        return self.world['start']