from flask import render_template, request, jsonify, current_app
from datetime import datetime
import openai

from apps.flirty_messages import bp
from config import OPENAI_API_KEY, API_PROVIDERS, DEFAULT_TEMPERATURE
from apps.flirty_messages.utils.prompt_builder import build_prompt

# Define dropdown options
AUDIENCE_OPTIONS = [
    "Casual (e.g., for light-hearted flirting or fun chats)",
    "Serious / Relationship-Focused",
    "Friends / Platonic",
    "Hookup / Short-term",
    "Family-friendly / Wholesome",
    "Other/Custom"
]

TONE_OPTIONS = [
    "Playful",
    "Cheesy / Corny",
    "Funny / Humorous",
    "Romantic / Sweet",
    "Poetic / Artistic",
    "Bold / Adventurous",
    "Sarcastic / Witty",
    "Mystical / Mysterious",
    "Sincere / Heartfelt",
    "Other/Custom"
]

PURPOSE_OPTIONS = [
    "Icebreaker / Conversation Starter",
    "Compliment",
    "Confession of Feelings",
    "Cheer-Up / Encouragement",
    "Inside Joke Reference",
    "Apology",
    "Teasing / Banter",
    "Romantic Gesture",
    "Serious / Deep Connection",
    "Other/Custom"
]

TRAITS_OPTIONS = [
    "Athletic / Sports Lover",
    "Bookish / Nerdy",
    "Artistic / Creative",
    "Foodie / Culinary Enthusiast",
    "Music Lover / Audiophile",
    "Outdoor Enthusiast / Adventurous",
    "Tech-Savvy / Geeky",
    "Fashion-Conscious / Trendy",
    "Animal Lover / Pet Parent",
    "Traveler / Wanderlust",
    "Introverted",
    "Extroverted",
    "Spiritual / Mindful",
    "Ambitious / Workaholic",
    "Gamer",
    "Movie Buff",
    "Other/Custom"
]

EMOTIONS_OPTIONS = [
    "Love",
    "Infatuation / Crush",
    "Admiration",
    "Curiosity",
    "Excitement",
    "Playful Interest",
    "Longing / Desire",
    "Nervousness",
    "Comfort / Warmth",
    "Joy / Happiness",
    "Flattered",
    "Tenderness",
    "Other/Custom"
]

CONTEXT_OPTIONS = [
    "First Meeting / First Date",
    "Online Chat / Dating App",
    "Long-Distance Relationship",
    "In-Person / Real-Life Encounter",
    "Social Media DM",
    "Birthday",
    "Anniversary",
    "Late-Night Text",
    "Valentine's Day",
    "Holiday / Festive",
    "Office / Work Setting",
    "Random Surprise",
    "Other/Custom"
]

THEMES_OPTIONS = [
    "Nature-Inspired (flowers, sunsets, stars, etc.)",
    "Food-Inspired (desserts, coffee, spicy, sweet, etc.)",
    "Pop Culture (movies, TV shows, memes, trends, etc.)",
    "Music / Song Lyrics",
    "Tech / Geeky (puns about apps, coding, gadgets, etc.)",
    "Historical / Literary References",
    "Fantasy / Mythology (dragons, gods, magical realms)",
    "Seasonal / Holiday (Christmas, Halloween, etc.)",
    "Travel / Exotic Locations",
    "Celebrity / Influencer Reference",
    "Sports / Team Spirit",
    "Other/Custom"
]

LANGUAGE_OPTIONS = [
    "English",
    "Spanish",
    "French",
    "German",
    "Italian",
    "Portuguese",
    "Chinese (Mandarin)",
    "Japanese",
    "Korean",
    "Hindi",
    "Arabic",
    "Russian",
    "Nepali",
    "Other/Custom"
]

STYLE_OPTIONS = [
    "Highly Creative / Poetic",
    "Straightforward / Direct",
    "Cheesy / Pun-Filled",
    "Classy / Refined",
    "Playful / Lighthearted",
    "Witty / Sarcastic",
    "Edgy",
    "Romantic / Sweeping",
    "Friendly / Casual",
    "Other/Custom"
]

NUM_LINES_OPTIONS = ["1", "2", "3", "4", "5"]

def log_interaction(audience, tone, purpose, traits, emotions, context, themes, language, style, num_lines, generated_text):
    """
    Log user input selections and the generated text to the application log
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"""
--- FLIRTY MESSAGE LOG ---
Timestamp: {timestamp}
AUDIENCE: {audience}
TONE: {tone}
PURPOSE: {purpose}
TRAITS: {traits}
EMOTIONS: {emotions}
CONTEXT: {context}
THEMES: {themes}
LANGUAGE: {language}
STYLE: {style}
NUMBER_OF_LINES: {num_lines}

Generated Text:
{generated_text}
------------------------
"""
    current_app.logger.info(log_entry)

@bp.route('/')
def index():
    """Home page for flirty messages generator"""
    # Convert API_PROVIDERS dictionary to format usable by the template
    api_providers = list(API_PROVIDERS.keys())
    api_models = {provider: info["models"] for provider, info in API_PROVIDERS.items()}
    
    return render_template(
        'flirty/index.html',
        audience_options=AUDIENCE_OPTIONS,
        tone_options=TONE_OPTIONS,
        purpose_options=PURPOSE_OPTIONS,
        traits_options=TRAITS_OPTIONS,
        emotions_options=EMOTIONS_OPTIONS,
        context_options=CONTEXT_OPTIONS,
        themes_options=THEMES_OPTIONS,
        language_options=LANGUAGE_OPTIONS,
        style_options=STYLE_OPTIONS,
        num_lines_options=NUM_LINES_OPTIONS,
        api_providers=api_providers,
        api_models=api_models
    )

@bp.route('/generate', methods=['POST'])
def generate():
    """Handle message generation"""
    try:
        # Get form data
        data = request.form
        audience = data.get('audience', AUDIENCE_OPTIONS[0])
        tone = data.get('tone', TONE_OPTIONS[0])
        purpose = data.get('purpose', PURPOSE_OPTIONS[0])
        traits = data.get('traits', TRAITS_OPTIONS[0])
        emotions = data.get('emotions', EMOTIONS_OPTIONS[0])
        context = data.get('context', CONTEXT_OPTIONS[0])
        themes = data.get('themes', THEMES_OPTIONS[0])
        language = data.get('language', LANGUAGE_OPTIONS[0])
        style = data.get('style', STYLE_OPTIONS[0])
        num_lines = data.get('num_lines', NUM_LINES_OPTIONS[0])
        api_provider = data.get('api_provider', 'OpenAI')
        
        # Check if the provider exists and get the first model as default
        if api_provider in API_PROVIDERS and API_PROVIDERS[api_provider]["models"]:
            default_model = API_PROVIDERS[api_provider]["models"][0]
        else:
            default_model = "gpt-3.5-turbo"
            
        api_model = data.get('api_model', default_model)
        additional_text = data.get('additional_text', '')
        
        # Build the prompt
        prompt = build_prompt(
            audience,
            tone,
            purpose,
            traits,
            emotions,
            context,
            themes,
            language,
            style,
            num_lines,
            additional_text
        )
        
        # Generate the message using OpenAI API
        generated_text = query_openai(prompt, api_model)
        
        # Log the interaction
        log_interaction(
            audience, tone, purpose, traits, emotions,
            context, themes, language, style, num_lines, generated_text
        )
        
        # Return as JSON for AJAX request
        return jsonify({
            'success': True, 
            'generated_text': generated_text
        })
        
    except Exception as e:
        current_app.logger.error(f"Error generating message: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

def query_openai(prompt, model="gpt-3.5-turbo", temperature=None):
    """
    Query the OpenAI API with the given prompt
    
    Args:
        prompt (str): The user-facing prompt string
        model (str): The model to use
        temperature (float, optional): Creativity parameter (0.0 to 1.0)
        
    Returns:
        str: The generated text or an error message
    """
    if temperature is None:
        temperature = DEFAULT_TEMPERATURE
        
    openai.api_key = OPENAI_API_KEY

    if not OPENAI_API_KEY:
        return "Error: No OpenAI API key found. Please set OPENAI_API_KEY in the environment."

    try:
        # Configure the client
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
        # Create the chat completion request
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a witty assistant who excels at writing playful, "
                        "romantic, and engaging messages. Provide concise, creative lines."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=temperature,
            max_tokens=150  # Enough for short messages
        )
        
        # Extract the assistant's message
        return response.choices[0].message.content.strip()
    except Exception as e:
        current_app.logger.error(f"OpenAI API Error: {str(e)}")
        return f"OpenAI API Error: {e}"