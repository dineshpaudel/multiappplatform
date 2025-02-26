from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class MessageGenerationForm(FlaskForm):
    """Form for generating flirty messages"""
    
    audience = SelectField(
        'Audience',
        validators=[DataRequired()]
    )
    
    tone = SelectField(
        'Tone',
        validators=[DataRequired()]
    )
    
    purpose = SelectField(
        'Purpose',
        validators=[DataRequired()]
    )
    
    traits = SelectField(
        'Recipient Traits',
        validators=[DataRequired()]
    )
    
    emotions = SelectField(
        'Emotions to Convey',
        validators=[DataRequired()]
    )
    
    context = SelectField(
        'Context',
        validators=[DataRequired()]
    )
    
    themes = SelectField(
        'Themes / References',
        validators=[DataRequired()]
    )
    
    language = SelectField(
        'Language',
        validators=[DataRequired()]
    )
    
    style = SelectField(
        'Style',
        validators=[DataRequired()]
    )
    
    num_lines = SelectField(
        'Number of Lines',
        validators=[DataRequired()],
        choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')]
    )
    
    api_provider = SelectField(
        'AI Provider',
        validators=[DataRequired()]
    )
    
    api_model = SelectField(
        'AI Model',
        validators=[DataRequired()]
    )
    
    additional_text = TextAreaField(
        'Additional Details (Optional)',
        validators=[Optional(), Length(max=500)],
        description='Add any custom details, specific references, or inside jokes'
    )
    
    submit = SubmitField('Generate Message')
    
    def set_choices(self, options_dict, api_providers, api_models):
        """Set dynamic choices for select fields"""
        self.audience.choices = [(opt, opt) for opt in options_dict.get('audience_options', [])]
        self.tone.choices = [(opt, opt) for opt in options_dict.get('tone_options', [])]
        self.purpose.choices = [(opt, opt) for opt in options_dict.get('purpose_options', [])]
        self.traits.choices = [(opt, opt) for opt in options_dict.get('traits_options', [])]
        self.emotions.choices = [(opt, opt) for opt in options_dict.get('emotions_options', [])]
        self.context.choices = [(opt, opt) for opt in options_dict.get('context_options', [])]
        self.themes.choices = [(opt, opt) for opt in options_dict.get('themes_options', [])]
        self.language.choices = [(opt, opt) for opt in options_dict.get('language_options', [])]
        self.style.choices = [(opt, opt) for opt in options_dict.get('style_options', [])]
        self.api_provider.choices = [(provider, provider) for provider in api_providers]
        self.api_model.choices = [(model, model) for model in api_models]