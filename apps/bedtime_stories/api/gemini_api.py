import google.generativeai as genai
from config import GEMINI_API_KEY, DEFAULT_TEMPERATURE
import logging

logger = logging.getLogger(__name__)

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def generate_story(prompt, model="gemini-pro", max_tokens=2000, temperature=None):
    """
    Generate a story using Google Gemini API
    
    Args:
        prompt (str): The story generation prompt
        model (str): Gemini model to use
        max_tokens (int): Maximum token length (approximate)
        temperature (float, optional): Creativity parameter (0.0 to 1.0)
        
    Returns:
        str: Generated story text
    """
    if temperature is None:
        temperature = DEFAULT_TEMPERATURE
        
    try:
        logger.info(f"Generating story with Gemini model: {model}")
        
        # Initialize the model
        generation_model = genai.GenerativeModel(model)
        
        # Prepare system instructions and prompt
        system_instruction = "You are a creative storyteller for bedtime stories."
        full_prompt = f"{system_instruction}\n\n{prompt}"
        
        # Generate content
        response = generation_model.generate_content(
            full_prompt,
            generation_config={
                "max_output_tokens": max_tokens,
                "temperature": temperature,
            }
        )
        
        return response.text
    except Exception as e:
        logger.error(f"Gemini API Error: {str(e)}")
        return f"Error generating story: {str(e)}"