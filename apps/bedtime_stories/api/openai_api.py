from openai import OpenAI
from config import OPENAI_API_KEY, DEFAULT_TEMPERATURE
import logging

logger = logging.getLogger(__name__)

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_story(prompt, model="gpt-3.5-turbo", max_tokens=2000, temperature=None):
    """
    Generate a story using OpenAI API
    
    Args:
        prompt (str): The story generation prompt
        model (str): OpenAI model to use
        max_tokens (int): Maximum token length
        temperature (float, optional): Creativity parameter (0.0 to 1.0)
        
    Returns:
        str: Generated story text
    """
    if temperature is None:
        temperature = DEFAULT_TEMPERATURE
        
    try:
        logger.info(f"Generating story with OpenAI model: {model}")
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a creative storyteller for bedtime stories."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"OpenAI API Error: {str(e)}")
        return f"Error generating story: {str(e)}"