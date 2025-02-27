from flask import Flask, render_template, redirect, url_for
import os
from dotenv import load_dotenv
import base64
from datetime import datetime

import json


creds_path = "/opt/render/project/.gcp_key.json"

if not os.path.exists(creds_path):
    print(f"❌ Google Cloud credentials file NOT found at: {creds_path}")
else:
    print(f"✅ Google Cloud credentials file exists at: {creds_path}")

print(f"GOOGLE_APPLICATION_CREDENTIALS: {os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')}")


creds_path = "/opt/render/project/.gcp_key.json"

# Get the base64 JSON string from environment
google_creds_b64 = os.environ.get("GOOGLE_TTS_JSON")

if google_creds_b64:
    # Decode and write the JSON key file
    google_creds = base64.b64decode(google_creds_b64).decode("utf-8")
    
    with open(creds_path, "w") as f:
        f.write(google_creds)
    
    # Set the environment variable for Google API
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds_path


# Load environment variables
load_dotenv()

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Configure app
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', os.urandom(24))
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')
    
    # Ensure necessary directories exist
    os.makedirs(os.path.join(app.root_path, 'logs'), exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Add current datetime to all templates
    @app.context_processor
    def inject_now():
        return {'now': datetime.now()}
    
    # Register main route
    @app.route('/')
    def index():
        return render_template('index.html')
    
    # Register error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error.html', error_code=404, error_message="Page not found"), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('error.html', error_code=500, error_message="Internal server error"), 500
    
    # Register blueprints for individual apps
    register_blueprints(app)
    
    return app

def register_blueprints(app):
    """Register blueprints for all available apps"""
    # Import app blueprints
    from apps.bedtime_stories import bp as bedtime_stories_bp
    from apps.flirty_messages import bp as flirty_messages_bp
    
    # Register app blueprints with URL prefixes
    app.register_blueprint(bedtime_stories_bp, url_prefix='/stories')
    app.register_blueprint(flirty_messages_bp, url_prefix='/flirty')

if __name__ == "__main__":
    app = create_app()  # Call the function to create the app
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
