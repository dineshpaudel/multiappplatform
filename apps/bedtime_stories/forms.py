from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class StoryGenerationForm(FlaskForm):
    """Form for generating bedtime stories"""
    
    story_length = SelectField(
        'Story Length',
        validators=[DataRequired()],
        choices=[
            ('5', '5 minutes'),
            ('10', '10 minutes'),
            ('15', '15 minutes'),
            ('30', '30 minutes')
        ]
    )
    
    age_group = SelectField(
        'Age Group',
        validators=[DataRequired()]
    )
    
    genre = SelectField(
        'Genre',
        validators=[DataRequired()]
    )
    
    api_provider = SelectField(
        'AI Provider',
        validators=[DataRequired()]
    )
    
    api_model = SelectField(
        'AI Model',
        validators=[DataRequired()]
    )
    
    custom_prompt = TextAreaField(
        'Custom Prompt (Optional)',
        validators=[Optional(), Length(max=1000)],
        description='Enter a custom prompt or specific story elements to include'
    )
    
    submit = SubmitField('Generate Story')

    def set_choices(self, age_groups, genres, api_providers, api_models):
        """Set dynamic choices for select fields"""
        self.age_group.choices = [(age, age) for age in age_groups]
        self.genre.choices = [(genre, genre) for genre in genres]
        self.api_provider.choices = [(provider, provider) for provider in api_providers]
        self.api_model.choices = [(model, model) for model in api_models]

class AudioGenerationForm(FlaskForm):
    """Form for generating audio from a story"""
    
    story_id = StringField('Story ID', validators=[DataRequired()])
    voice_name = SelectField('Voice', validators=[DataRequired()])
    speed = SelectField('Reading Speed', validators=[DataRequired()])
    submit = SubmitField('Generate Audio')
    
    def set_choices(self, voices, speeds):
        """Set dynamic choices for select fields"""
        self.voice_name.choices = [(voice['name'], voice['display_name']) for voice in voices]
        self.speed.choices = [(str(speed['value']), speed['display']) for speed in speeds]