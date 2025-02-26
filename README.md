# AI Content Generator Platform

A modular Flask-based web application platform hosting multiple AI-powered content generation tools.

## Features

- **Bedtime Story Generator**: Create personalized bedtime stories for various age groups with text-to-speech capabilities
- **Flirty Messages Generator**: Generate creative and customized messages for that special someone
- **Modular Architecture**: Easy to add new AI-powered tools as separate modules

## Setup and Installation

### Prerequisites

- Python 3.8+
- API keys for OpenAI, DeepSeek, and/or Google Gemini (depending on which services you want to use)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ai-content-generator.git
   cd ai-content-generator
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with your API keys:
   ```
   SECRET_KEY=your_secret_key
   OPENAI_API_KEY=your_openai_api_key
   DEEPSEEK_API_KEY=your_deepseek_api_key
   GEMINI_API_KEY=your_gemini_api_key
   DEBUG=True
   ```

5. For Google Text-to-Speech functionality:
   - Create a Google Cloud account and enable the Text-to-Speech API
   - Download your JSON credentials file and set the GOOGLE_APPLICATION_CREDENTIALS environment variable:
     ```
     export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your-credentials.json"
     ```

### Running the Application

Start the development server:
```
python app.py
```

Then visit `http://127.0.0.1:5000/` in your web browser.

## Project Structure

The application follows a modular architecture with each app functioning as a separate module:

```
multi_app_platform/
│
├── app.py                      # Main Flask application entry point
├── config.py                   # Shared configuration settings
├── apps/                       # Individual apps directory
│   ├── bedtime_stories/        # Bedtime Story Generator app
│   └── flirty_messages/        # Flirty Text Generator app
│
└── static/                     # Shared static files
    └── css/main.css            # Main styling for the platform
```

## Adding a New App

To add a new app to the platform:

1. Create a new directory under the `apps` folder with your app name
2. Create the necessary files (see existing apps for reference):
   - `__init__.py` - Define your Blueprint and initialize the app
   - `routes.py` - Define the routes for your app
   - `forms.py` - Define any forms needed for your app
   - Create appropriate templates in a subfolder under `templates`
   - Add app-specific static files if needed

3. Register your app's Blueprint in `app.py`

4. Add a card for your app on the homepage in `templates/index.html`

## License

[MIT License](LICENSE)