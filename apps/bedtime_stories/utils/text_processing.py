def count_words(text):
    """
    Count the number of words in a text
    
    Args:
        text (str): The text to count words in
        
    Returns:
        int: Number of words
    """
    return len(text.split())

def extract_title(story_text):
    """
    Extract title from the story text if available
    
    Args:
        story_text (str): The generated story text
        
    Returns:
        str: Extracted title or default title
    """
    lines = story_text.strip().split('\n')
    
    # Check if the first line looks like a title
    if lines and len(lines[0]) < 100 and not lines[0].endswith('.'):
        return lines[0].strip()
    
    # Look for a line that starts with "Title:"
    for line in lines[:5]:  # Only check first 5 lines
        if line.lower().startswith('title:'):
            return line.split(':', 1)[1].strip()
            
    return "Bedtime Story"

def create_export_text(story_text, genre, word_count):
    """
    Format story for export to text file
    
    Args:
        story_text (str): The story text
        genre (str): The story genre
        word_count (int): Number of words in the story
        
    Returns:
        str: Formatted text for export
    """
    title = extract_title(story_text)
    
    export_text = f"""TITLE: {title}
GENRE: {genre}
WORD COUNT: {word_count}

{story_text}
"""
    return export_text