system_prompt = """You are an AI Game Assistant. \
Your job is to detect changes to a player's \
inventory based on the most recent story and game state.
If a player picks up, or gains an item add it to the inventory \
with a positive change_amount.
If a player loses an item remove it from their inventory \
with a negative change_amount.
Given a player name, inventory and story, return a list of json update
of the player's inventory in the following form.
Only take items that it's clear the player (you) lost.
Only give items that it's clear the player gained. 
Don't make any other item updates.
If no items were changed return {"itemUpdates": []}
and nothing else.

Response must be in Valid JSON
Don't add items that were already added in the inventory

Inventory Updates:
{
    "itemUpdates": [
        {"name": <ITEM NAME>, 
        "change_amount": <CHANGE AMOUNT>}...
    ]
}
"""

def detect_inventory_changes(game_state, output):
    
    inventory = game_state['inventory']
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": 
         f'Current Inventory: {str(inventory)}'},
        
        {"role": "user", "content": f'Recent Story: {output}'},
        {"role": "user", "content": 'Inventory Updates'}
    ]
    chat_completion = client.chat.completions.create(
        # response_format={"type": "json_object", "schema": InventoryUpdate.model_json_schema()},
        model="meta-llama/Llama-3-70b-chat-hf",
        temperature=0.0,
        messages=messages
    )
    response = chat_completion.choices[0].message.content
    result = json.loads(response)
    return result['itemUpdates']


def update_inventory(inventory, item_updates):
    update_msg = ''
    
    for update in item_updates:
        name = update['name']
        change_amount = update['change_amount']
        
        if change_amount > 0:
            if name not in inventory:
                inventory[name] = change_amount
            else:
                inventory[name] += change_amount
            update_msg += f'\nInventory: {name} +{change_amount}'
        elif name in inventory and change_amount < 0:
            inventory[name] += change_amount
            update_msg += f'\nInventory: {name} {change_amount}'
            
        if name in inventory and inventory[name] < 0:
            del inventory[name]
            
    return update_msg