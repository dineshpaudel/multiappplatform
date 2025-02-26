from flask import Blueprint

# Create Blueprint for the bedtime stories app
bp = Blueprint(
    'bedtime_stories', 
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/stories/static'
)

# Import routes at the bottom to avoid circular imports
from apps.bedtime_stories import routes