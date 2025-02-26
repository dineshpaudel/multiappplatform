import os

def create_required_directories():
    """Create all required directories for the application"""
    
    # Main directories
    directories = [
        'templates',
        'static',
        'static/css',
        'static/js',
        'static/images',
        'logs',
        'uploads',
        'apps',
    ]
    
    # Bedtime Stories app directories
    bedtime_dirs = [
        'apps/bedtime_stories',
        'apps/bedtime_stories/templates',
        'apps/bedtime_stories/templates/stories',
        'apps/bedtime_stories/static',
        'apps/bedtime_stories/static/css',
        'apps/bedtime_stories/static/js',
        'apps/bedtime_stories/static/audio',
        'apps/bedtime_stories/static/exports',
        'apps/bedtime_stories/utils',
        'apps/bedtime_stories/api',
    ]
    
    # Flirty Messages app directories
    flirty_dirs = [
        'apps/flirty_messages',
        'apps/flirty_messages/templates',
        'apps/flirty_messages/templates/flirty',
        'apps/flirty_messages/static',
        'apps/flirty_messages/static/css',
        'apps/flirty_messages/static/js',
        'apps/flirty_messages/utils',
    ]
    
    # Create all directories
    for directory in directories + bedtime_dirs + flirty_dirs:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

if __name__ == "__main__":
    create_required_directories()
    print("All required directories created successfully!")