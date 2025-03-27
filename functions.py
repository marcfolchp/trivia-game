import cohere
import json
import random
import hashlib
from pymongo import MongoClient
import streamlit as st
from dotenv import load_dotenv
import os

# --------- CREDENTIALS ---------

db_user = st.secrets["db_user"]
db_pass = st.secrets["db_pass"]
api_key = st.secrets["api_key"]

# --------- GAME ---------

trivia_categories = {
    "Geography": [
        "Capital cities of the world",
        "Famous rivers and lakes",
        "Mountain ranges",
        "Deserts of the world",
        "Countries and their official languages",
        "World landmarks",
        "Oceans and seas",
        "World time zones",
        "Countries with the largest populations",
        "Famous world cities",
        "Largest countries by area",
        "Smallest countries in the world",
        "UNESCO World Heritage sites",
        "Countries with the longest coastlines",
        "Volcanoes and tectonic plates",
        "World's highest mountains",
        "Famous islands",
        "National parks around the world",
        "Extreme weather zones",
        "Natural wonders of the world"
    ],
    
    "History": [
        "Ancient civilizations",
        "World War I",
        "World War II",
        "The Cold War",
        "Famous revolutions",
        "The Renaissance",
        "Medieval history",
        "Famous leaders and emperors",
        "The American Revolution",
        "The French Revolution",
        "Colonialism and independence",
        "The rise and fall of the Roman Empire",
        "The Industrial Revolution",
        "Famous historical battles",
        "The history of the United Nations",
        "World-changing treaties",
        "Historical monuments",
        "Famous historical speeches",
        "The history of slavery",
        "The history of democracy"
    ],
    
    "Science": [
        "The Periodic Table of Elements",
        "The Theory of Evolution",
        "Famous scientists and their discoveries",
        "Physics laws",
        "Space exploration",
        "The human brain and nervous system",
        "Types of clouds",
        "Climate change and global warming",
        "Medical breakthroughs",
        "Inventions and inventors",
        "Astronomy and celestial bodies",
        "Biology and ecosystems",
        "Chemistry and chemical reactions",
        "The water cycle",
        "Genetics and DNA",
        "Electricity and magnetism",
        "The digestive system",
        "Physics of motion",
        "Human anatomy",
        "The laws of thermodynamics"
    ],
    
    "Entertainment": [
        "Oscar-winning movies",
        "Famous actors and actresses",
        "Classic TV shows",
        "Music history and genres",
        "Famous books and authors",
        "Popular video games",
        "Broadway musicals",
        "Disney animated movies",
        "Pop culture trends",
        "Famous directors",
        "Television series of the 90s",
        "Famous singers and bands",
        "Musical instruments",
        "The history of rock and roll",
        "The Beatles and their legacy",
        "Famous movie quotes",
        "Film noir genre",
        "Famous authors and poets",
        "History of cinema",
        "Superhero comic book characters"
    ],
    
    "Sports": [
        "The Olympic Games",
        "FIFA World Cup",
        "NBA history",
        "Super Bowl champions",
        "Tennis Grand Slam winners",
        "Formula 1 racing",
        "Baseball Hall of Fame",
        "Famous athletes",
        "The history of boxing",
        "The Tour de France",
        "World records in sports",
        "The history of the NBA",
        "Soccer legends",
        "The Wimbledon tournament",
        "Famous sports rivalries",
        "The history of rugby",
        "The NFL draft",
        "The history of the Winter Olympics",
        "The greatest football teams",
        "The history of the UFC"
    ],
    
    "Literature": [
        "Shakespeare's plays",
        "Famous novels of the 19th century",
        "Classic children's books",
        "Poetry and poets",
        "The works of Jane Austen",
        "Science fiction novels",
        "Famous detectives in literature",
        "Famous literary awards",
        "The Harry Potter series",
        "Fantasy literature",
        "Famous non-fiction books",
        "The history of the novel",
        "The works of Charles Dickens",
        "The romantic period in literature",
        "Famous book series",
        "Myths and legends in literature",
        "Famous literary characters",
        "Literary genres",
        "Bestselling authors of the 20th century",
        "Famous short stories"
    ],
    
    "Art": [
        "The Renaissance art movement",
        "Famous painters and their works",
        "Impressionist art",
        "Cubism in art",
        "Modern art movements",
        "Sculpture and its history",
        "Famous art museums",
        "The history of photography",
        "The role of color in art",
        "Art from Ancient Greece and Rome",
        "Street art and graffiti",
        "Art of the 20th century",
        "Famous art forgeries",
        "Abstract expressionism",
        "Art restoration techniques",
        "Famous art exhibitions",
        "The use of perspective in art",
        "The evolution of portraiture",
        "Art and politics",
        "The history of architecture"
    ],
    
    "Music": [
        "Classical music composers",
        "The history of jazz",
        "Rock and roll history",
        "Famous musical instruments",
        "The history of opera",
        "Pop music trends",
        "The history of blues",
        "Famous music festivals",
        "Music theory basics",
        "The evolution of music genres",
        "Famous music producers",
        "The Beatles and their impact",
        "The history of hip-hop",
        "Music and cultural movements",
        "Musical collaborations",
        "Famous orchestras",
        "The development of musical notation",
        "The role of women in music",
        "Music technology advancements",
        "The Grammy Awards"
    ]
}

def create_question():

    random_category = random.choice(list(trivia_categories.keys()))  # Random category
    random_topic = random.choice(trivia_categories[random_category])  # Random topic from that category

    prompt = f"""
    Generate a random true or false trivia question on general world knowledge.
    The category is: {random_category}
    The topic is: {random_topic} 
    The difficulty should be relatively easy.  
    Ensure the question is unique and not similar to any previously generated ones.  
    Return the response in the following JSON format without any extra text:  

    {{
    "question": "<Your trivia question here>",
    "answer": true or false,
    "category": "<category given here>",
    "topic": "<topic given here>"
    }}
    """

    co = cohere.ClientV2(api_key)
    response = co.chat(
        model="command-a-03-2025", 
        messages=[{"role": "user", "content": prompt}]
    )

    message = response.message
    content_list = message.content

    json_string = content_list[0].text

    json_response = json.loads(json_string)

    return json_response

# --------- STREAMLIT ---------

uri = f"mongodb+srv://{db_user}:{db_pass}@cluster0.pxpov.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client['capitals-game']
users_collection = db['capitals-game']

def check_credentials(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    user = users_collection.find_one({'username': username, 'password': hashed_password})
    return user

def register_user(username, password):
    existing_user = users_collection.find_one({'username': username})
    if existing_user:
        return False
    
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    users_collection.insert_one({'username': username, 'password': hashed_password})
    return True

def switch_page(page):
    st.session_state["page"] = page
    st.rerun()

def login(page, user):
    st.session_state["page"] = page
    st.session_state["username"] = user
    st.rerun()

def add_one(username, column):
    users_collection.update_one(
    {"username": username},
    {"$inc": {column: 1}}
    )

def handle_answer(user_answer, question):
    correct_answer = question["answer"]
    category = question["category"]

    # Update score based on correctness
    if user_answer == correct_answer:
        add_one(st.session_state["username"], category)
        add_one(st.session_state["username"], "total")
    else:
        add_one(st.session_state["username"], "total")

    # Generate and store a new question
    st.session_state["current_question"] = create_question()

    # Force a rerun to display the new question
    st.experimental_rerun()