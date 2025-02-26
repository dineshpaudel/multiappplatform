import os
from google.cloud import texttospeech
import logging

logger = logging.getLogger(__name__)

def generate_audio(text, output_file, voice_name="en-US-Standard-D", speaking_rate=1.0):
    """
    Convert text to speech using Google TTS API
    
    Args:
        text (str): The text to convert to speech
        output_file (str): Path to save the audio file
        voice_name (str): Name of the voice to use
        speaking_rate (float): Speed of the speech (0.5 to 2.0)
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Initialize TTS client
        client = texttospeech.TextToSpeechClient()
        
        logger.info(f"Generating audio with voice: {voice_name}, speed: {speaking_rate}")
        
        # Set the text input
        synthesis_input = texttospeech.SynthesisInput(text=text)
        
        # Build the voice request
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name=voice_name
        )
        
        # Select the audio file type and configure speed
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=speaking_rate,
            pitch=0.0
        )
        
        # Perform the text-to-speech request
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Write the response to the output file
        with open(output_file, "wb") as out:
            out.write(response.audio_content)
        
        logger.info(f"Successfully generated audio at: {output_file}")
        return True
        
    except Exception as e:
        logger.error(f"TTS API Error: {str(e)}")
        logger.error(f"Error details: {type(e).__name__}")
        return False