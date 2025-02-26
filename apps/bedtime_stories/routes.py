from flask import render_template, request, jsonify, session, send_file, current_app, url_for
import os
import uuid
from datetime import datetime
import importlib

from apps.bedtime_stories import bp
from config import API_PROVIDERS, TTS_VOICES, TTS_SPEEDS

# Import app-specific utilities
from apps.bedtime_stories.utils.text_processing import count_words, create_export_text
from apps.bedtime_stories.utils.tts import generate_audio

# Define story length options
STORY_LENGTHS = {
    "5": 300,     # ~300 words for 5 min story
    "10": 600,    # ~600 words for 10 min story
    "15": 900,    # ~900 words for 15 min story
    "30": 1800,   # ~1800 words for 30 min story
}

# Age Groups
AGE_GROUPS = [
    "Toddler (2-3 years)",
    "Preschool (3-5 years)",
    "Early Elementary (5-7 years)",
    "Late Elementary (8-10 years)",
    "Middle School (11-13 years)",
    "High School (14-18 years)",
    "Adult (21 years and older)"
]

# Genres by Age Group
GENRES_BY_AGE_GROUP = {
    "Toddler (2-3 years)": [
        "Animal Stories",
        "Bedtime Rhymes",
        "Simple Adventures",
        "Lullaby Stories",
        "Everyday Discoveries"
    ],
    "Preschool (3-5 years)": [
        "Fairy Tales",
        "Magical Friends",
        "Playful Adventures",
        "Simple Fables",
        "Talking Animals",
        "Wonder and Discovery"
    ],
    "Early Elementary (5-7 years)": [
        "Friendship Stories",
        "Magical Quests",
        "Funny Adventures",
        "Simple Fantasy",
        "Animal Heroes",
        "Everyday Magic"
    ],
    "Late Elementary (8-10 years)": [
        "Adventure Stories",
        "Mystery Tales",
        "Fantasy Worlds",
        "Superhero Stories",
        "Historical Adventures",
        "Magical Creatures"
    ],
    "Middle School (11-13 years)": [
        "Fantasy Quests",
        "Science Fiction",
        "Coming of Age",
        "Mythological Adventures",
        "Mystery & Detective",
        "Historical Fiction",
        "Magical Realism"
    ],
    "High School (14-18 years)": [
        "Dystopian",
        "Science Fiction",
        "Contemporary Fiction",
        "Mystery/Thriller",
        "Fantasy Adventure",
        "Romance",
        "Historical Fiction"
    ],
    "Adult (21 years and older)": [
        "Literary Fiction",
        "Mystery & Detective",
        "Science Fiction",
        "Fantasy",
        "Romance",
        "Historical Fiction",
        "Thriller",
        "Horror"
    ]
}

def cleanup_audio_files():
    """Clean up temporary audio files"""
    try:
        audio_dir = os.path.join(current_app.root_path, 'apps/bedtime_stories/static/audio')
        if os.path.exists(audio_dir):
            for file in os.listdir(audio_dir):
                if file.endswith('.mp3'):
                    try:
                        os.remove(os.path.join(audio_dir, file))
                    except Exception as e:
                        print(f"Error removing file {file}: {e}")
    except Exception as e:
        print(f"Error during cleanup: {e}")

@bp.route('/')
def index():
    """Home page route - displays story generation form"""
    # Clean up any existing audio files when returning to home
    cleanup_audio_files()
    
    # Get default selections
    default_age_group = AGE_GROUPS[1]  # Preschool by default
    default_genres = GENRES_BY_AGE_GROUP[default_age_group]
    
    # Convert API_PROVIDERS dictionary to format usable by the template
    api_providers = list(API_PROVIDERS.keys())
    api_models = {provider: info["models"] for provider, info in API_PROVIDERS.items()}
    
    return render_template(
        'stories/index.html',
        story_lengths=list(STORY_LENGTHS.keys()),
        genres=default_genres,
        age_groups=AGE_GROUPS,
        api_providers=api_providers,
        api_models=api_models
    )

@bp.route('/get_genres/<age_group>', methods=['GET'])
def get_genres(age_group):
    """API endpoint to get genres for selected age group"""
    try:
        genres = GENRES_BY_AGE_GROUP.get(age_group, [])
        return jsonify({'genres': genres})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/get_models/<provider>', methods=['GET'])
def get_models(provider):
    """API endpoint to get models for selected provider"""
    try:
        if provider in API_PROVIDERS:
            models = API_PROVIDERS[provider]["models"]
            return jsonify({'models': models})
        return jsonify({'models': []})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/generate', methods=['POST'])
def generate():
    """Handle story generation"""
    try:
        # Get form data
        data = request.form
        story_length = data.get('story_length', '10')
        genre = data.get('genre', 'Fantasy')
        age_group = data.get('age_group', 'Preschool (3-5 years)')
        api_provider = data.get('api_provider', 'OpenAI')
        
        # Check if the provider exists and get the first model as default
        if api_provider in API_PROVIDERS and API_PROVIDERS[api_provider]["models"]:
            default_model = API_PROVIDERS[api_provider]["models"][0]
        else:
            default_model = "gpt-3.5-turbo"
            
        api_model = data.get('api_model', default_model)
        custom_prompt = data.get('custom_prompt', '')
        
        # Calculate target word count
        target_word_count = STORY_LENGTHS.get(story_length, 600)
        
        # Create generation prompt
        if custom_prompt:
            prompt = custom_prompt
        else:
            prompt = f"""
            Write a bedtime story with these specifications:
            - Genre: {genre}
            - Target audience: {age_group}
            - Approximate length: {target_word_count} words
            
            The story should be calming and appropriate for bedtime. Include a title at the beginning.
            """
        
        # Generate the story using selected API
        try:
            api_module = importlib.import_module(f"apps.bedtime_stories.api.{api_provider.lower()}_api")
            story = api_module.generate_story(
                prompt=prompt,
                model=api_model,
                max_tokens=target_word_count * 4
            )
        except ImportError:
            # Fallback to OpenAI if the selected provider's module doesn't exist
            api_module = importlib.import_module("apps.bedtime_stories.api.openai_api")
            story = api_module.generate_story(
                prompt=prompt,
                model="gpt-3.5-turbo",
                max_tokens=target_word_count * 4
            )
        
        # Process the generated story
        word_count = count_words(story)
        session_id = str(uuid.uuid4())
        
        # Store in session for later use
        session['story'] = {
            'id': session_id,
            'text': story,
            'genre': genre,
            'word_count': word_count,
            'timestamp': datetime.now().isoformat()
        }
        
        return render_template(
            'stories/story.html',
            story=story,
            word_count=word_count,
            story_id=session_id,
            tts_voices=TTS_VOICES,
            tts_speeds=TTS_SPEEDS
        )
        
    except Exception as e:
        current_app.logger.error(f"Error generating story: {str(e)}")
        return render_template('error.html', error_code=500, error_message=f"Error generating story: {str(e)}"), 500

@bp.route('/generate_audio', methods=['POST'])
def generate_audio_route():
    """Generate audio file with specified voice and speed"""
    try:
        # Get parameters
        story_id = request.form.get('story_id')
        voice_name = request.form.get('voice_name', 'en-US-Standard-D')
        speed = float(request.form.get('speed', '1.0'))
        
        # Validate story exists in session
        story_data = session.get('story', {})
        if story_data.get('id') != story_id:
            return jsonify({'error': 'Story not found'}), 404
        
        # Clean up existing audio files
        cleanup_audio_files()
        
        # Generate new audio file
        audio_dir = os.path.join(current_app.root_path, 'apps/bedtime_stories/static/audio')
        os.makedirs(audio_dir, exist_ok=True)
        
        audio_path = f"{story_id}.mp3"
        full_path = os.path.join(audio_dir, audio_path)
        
        success = generate_audio(
            story_data['text'], 
            output_file=full_path,
            voice_name=voice_name,
            speaking_rate=speed
        )
        
        if success:
            # Change this line to use the correct URL for static files
            return jsonify({
                'success': True,
                'audio_path': url_for('bedtime_stories.static', filename=f'audio/{audio_path}')
            })
        else:
            return jsonify({'error': 'Failed to generate audio'}), 500
        
    except Exception as e:
        current_app.logger.error(f"Error in generate_audio_route: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/export/<story_id>', methods=['GET'])
def export_story(story_id):
    """Export story as text file"""
    try:
        story_data = session.get('story', {})
        
        if story_data.get('id') != story_id:
            return jsonify({'error': 'Story not found'}), 404
            
        # Create formatted text for export
        export_text = create_export_text(
            story_data['text'],
            story_data['genre'],
            story_data['word_count']
        )
        
        # Create exports directory if it doesn't exist
        exports_dir = os.path.join(current_app.root_path, 'apps/bedtime_stories/static/exports')
        os.makedirs(exports_dir, exist_ok=True)
        
        # Save and send file
        export_file = os.path.join(exports_dir, f"{story_id}.txt")
        with open(export_file, 'w', encoding='utf-8') as f:
            f.write(export_text)
            
        return send_file(
            export_file,
            as_attachment=True,
            download_name="bedtime_story.txt"
        )
        
    except Exception as e:
        current_app.logger.error(f"Error exporting story: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/download_audio/<story_id>', methods=['GET'])
def download_audio(story_id):
    """Download generated audio file"""
    try:
        audio_file = os.path.join(current_app.root_path, f"apps/bedtime_stories/static/audio/{story_id}.mp3")
        
        if not os.path.exists(audio_file):
            return jsonify({'error': 'Audio file not found'}), 404
            
        return send_file(
            audio_file,
            as_attachment=True,
            download_name="bedtime_story.mp3"
        )
        
    except Exception as e:
        current_app.logger.error(f"Error downloading audio: {str(e)}")
        return jsonify({'error': str(e)}), 500