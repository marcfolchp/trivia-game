# Trivia Game Web App 🎮

A fun and interactive trivia game web application built with **Streamlit** and powered by **Cohere AI** for generating true/false general knowledge questions. Users can log in, track their performance, and compete globally in a ranking system based on accuracy.

## Features ✨

- 🔐 **User Authentication** – Log in to access your personal dashboard.
- ❓ **Trivia Gameplay** – Answer true/false questions on general knowledge topics.
- 🏠 **Home Page** – Displays trivia questions with TRUE/FALSE buttons.
- 📊 **My Stats** – View your performance across different trivia categories.
- 🌍 **Global Ranking** – See how you stack up against other players based on your percentage of correct answers.
- 🧠 **AI-Powered Questions** – Cohere generates varied and challenging trivia prompts.

## Tech Stack 🛠️

- **Frontend**: Streamlit  
- **Backend**: Python  
- **Database**: MongoDB  
- **AI Integration**: Cohere API

## Live Demo 🚀

Check out the live app here (doesn't work with ESADE's WiFi): [Launch Trivia Game](https://your-streamlit-url)

> No installation needed – just open the link in your browser.

## Project Structure 🧩

Here’s how the app is organized:

```
📁 trivia_game/
├── app.py             # Main Streamlit app interface
├── functions.py       # Core functions for authentication, question handling, stats, etc.
├── requirements.txt   # List of all required Python libraries
```

- **`app.py`**: Runs the UI using Streamlit and connects all game components.
- **`functions.py`**: Contains helper functions for login, question generation, stat tracking, database interactions, etc.
- **`requirements.txt`**: All dependencies needed to run the app locally (for development or deployment).

## Usage 🧪

- Visit the Home page to start answering questions.
- Check the My Stats page to review your accuracy by category.
- Head over to the Global Ranking page to see where you stand among all users.