# src/generate_world.py
from together import Together
from utils.helper import get_together_api_key
from world_builder.generator import WorldGenerator

def main():
    # Initialize the Together client
    client = Together(api_key=get_together_api_key())
    
    # Create world generator
    generator = WorldGenerator(client)
    
    # Generate complete world
    world = generator.generate_complete_world()
    
    # Generate game start
    generator.generate_game_start()
    
    # Save the world
    generator.save_world('../data/worlds/YourWorld_L1.json')
    
    print("World generation complete!")

if __name__ == "__main__":
    main()