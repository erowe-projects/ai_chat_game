# AI Chat Game

This is an AI chat game based off of the tutorial https://learn.deeplearning.ai/courses/building-an-ai-powered-game/lesson/1/introduction created by the Together.AI, AI Dungeon, and Deeplearning.AI. That provided the basis for a basic hierarchical world-generation, along with safety precautions, inventory-state management, and a basic chat UI powered by Gradio. 

Now, we are working on better summarization, world-state management, character state-management, story arcs etc. The eventual goal is to be able to provide approximately 20 hours of cohesive, accurate, and engaging story-telling. 

## Setup

```bash
# Clone the repository
git clone https://github.com/erowe-projects/ai_chat_game

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt