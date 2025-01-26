import os
import json
from dotenv import load_dotenv
import gradio as gr

# Environment and API functions
def load_env():
    """Load environment variables from .env file"""
    load_dotenv()

def get_together_api_key():
    """Get Together API key from environment variables"""
    load_env()
    return os.getenv('TOGETHER_API_KEY')

# World state management functions
def load_world(filename):
    """Load world data from JSON file"""
    with open(filename, 'r') as f:
        return json.load(f)

def save_world(world, filename):
    """Save world data to JSON file"""
    with open(filename, 'w') as f:
        json.dump(world, f)

#Safety checker function
def is_safe (message):
    prompt = f"""[INST] Task: Check if there is unsafe content in 
    'user' messages in conversations according to our safety policy 
    with the below categories.
    
    <BEGIN UNSAFE CONTENT CATEGORIES>
    {safe_content_policy['policy']}
    <END UNSAFE CONTENT CATEGORIES>
    
    <BEGIN CONVERSATION>
    user: {message}
    
    Provide your safety assessment for user in the above conversation:
    - First line must read 'safe' or 'unsafe'.
    - If unsafe, a second line must include a comma-separated list of 
    violated categories. [/INST]"""

    response = client.completions.create(
        model="Meta-Llama/LlamaGuard-2-8b",
        prompt=prompt,
    )

    result = response.choices[0].text
    return result.strip() == 'safe'

def get_game_state():
    """Get the current game state"""
    # Load the world file - update filename as needed
    world = load_world('../shared_data/YourWorld_L1.json')
    
    # Update these values to match your generated world structure
    kingdom = world['kingdoms']['YOUR_KINGDOM_NAME']
    town = kingdom['towns']["YOUR_TOWN_NAME"]
    character = town['npcs']['YOUR_CHARACTER_NAME']
    
    return {
        "world": world['description'],
        "kingdom": kingdom['description'],
        "town": town['description'],
        "character": character['description'],
        "start": world['start']
    }

def run_action(message, history, game_state):
    
    if(message == 'start game'):
        return game_state['start']
        
    system_prompt = """You are an AI Game master. Your job is to write what \
happens next in a player's adventure game.\
Instructions: \
You must on only write 1-3 sentences in response. \
Always write in second person present tense. \
Ex. (You look north and see...) \
Don't let the player use items they don't have in their inventory.
"""

    world_info = f"""
World: {game_state['world']}
Kingdom: {game_state['kingdom']}
Town: {game_state['town']}
Your Character:  {game_state['character']}
Inventory: {json.dumps(game_state['inventory'])}"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": world_info}
    ]

    for action in history:
        messages.append({"role": "assistant", "content": action[0]})
        messages.append({"role": "user", "content": action[1]})
           
    messages.append({"role": "user", "content": message})
    client = Together(api_key=get_together_api_key())
    model_output = client.chat.completions.create(
        model="meta-llama/Llama-3-70b-chat-hf",
        messages=messages
    )
    
    result = model_output.choices[0].message.content
    return result

# UI functions
def start_game(main_loop, share=False):
    # added code to support restart
    global demo
    # If demo is already running, close it first
    if demo is not None:
        demo.close()

    demo = gr.ChatInterface(
        main_loop,
        chatbot=gr.Chatbot(height=250, placeholder="Type 'start game' to begin"),
        textbox=gr.Textbox(placeholder="What do you do next?", container=False, scale=7),
        title="AI RPG",
        # description="Ask Yes Man any question",
        theme="soft",
        examples=["Look around", "Continue the story"],
        cache_examples=False,
        retry_btn="Retry",
        undo_btn="Undo",
        clear_btn="Clear",
                           )
    demo.launch(share=share, server_name="0.0.0.0")