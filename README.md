# C++ Learning Game

This small project is an interactive C++ learning game built with Streamlit.

## Features

- Levels of increasing difficulty
- Randomly generated C++ challenges
- Code editor with syntax highlighting
- Automated code evaluation
- Hints and solution suggestions.
- Test cases for each challenge

## Setup

1. Clone this repository
2. Install required dependencies:
pip install -r requirements.txt
3. Set up your API keys:
- Get API keys for Groq and DeepInfra (or another provider compatible with the OpenAI API, in that case change the `base_url`).
- Replace `YOUR_API_KEY` in the `game.py` file with your actual API keys

## Usage

1. Run the Streamlit app:
streamlit run game.py
2. The app will open in your default web browser
3. You will see your current level and a C++ challenge
4. Type your solution in the code editor on the right
5. Click "Submit" to submit your code for evaluation
6. It's time for us to get to it.
7. Click "Next Level" to advance to the next challenge

## How it works

The game uses AI LLM models for general challenges, evaluates the code, and provides feedback.

## Note

This game requires an active internet connection and uses API calls for general content and evaluating code. 
For now it only works in Spanish, feel free to change the language.
Made with the help of Claude 3.5 Sonnet.
