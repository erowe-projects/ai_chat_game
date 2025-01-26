
from utils.helper import (start_game, get_game_state, is_safe, run_action)

game_state = get_game_state(inventory={
    "cloth pants": 1,
    "cloth shirt": 1,
    "goggles": 1,
    "leather bound journal": 1,
    "gold": 5
})

def main_loop(message, history):
    output = run_action(message, history, game_state)
    
    safe = is_safe(output)
    if not safe:
        return 'Invalid Output'

    item_updates = detect_inventory_changes(game_state, output)
    update_msg = update_inventory(
        game_state['inventory'], 
        item_updates
    )
    output += update_msg

    return output

start_game(main_loop, True)