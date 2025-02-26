from flask import Blueprint

# Create Blueprint for the flirty messages app
bp = Blueprint(
    'flirty_messages', 
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/flirty/static'
)

# Import routes at the bottom to avoid circular imports
from apps.flirty_messages import routes