import requests
import json
from config import DEEPSEEK_API_KEY, DEFAULT_TEMPERATURE
import logging

logger = logging.getLogger(__name__)

def generate_story(prompt, model="deepseek-chat", max_tokens=2000, temperature=None):
    """
    Generate a story using DeepSeek API
    
    Args:
        prompt (str): The story generation prompt
        model (str): DeepSeek model to use
        max_tokens (int): Maximum token length
        temperature (float, optional): Creativity parameter (0.0 to 1.0)
        
    Returns:
        str: Generated story text
    """
    if temperature is None:
        temperature = DEFAULT_TEMPERATURE
        
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a creative storyteller for bedtime stories."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    
    try:
        logger.info(f"Generating story with DeepSeek model: {model}")
        
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload)
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        logger.error(f"DeepSeek API Error: {str(e)}")
        return f"Error generating story: {str(e)}"