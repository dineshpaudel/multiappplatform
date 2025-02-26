from datetime import datetime

class Story:
    """
    Model class for a generated bedtime story
    
    Note: This is a simple in-memory model.
    For persistence, this would be replaced with a database model.
    """
    
    def __init__(self, id, text, genre, age_group, word_count):
        """
        Initialize a new Story instance
        
        Args:
            id (str): Unique identifier for the story
            text (str): The generated story text
            genre (str): The story genre
            age_group (str): Target age group for the story
            word_count (int): Number of words in the story
        """
        self.id = id
        self.text = text
        self.genre = genre
        self.age_group = age_group
        self.word_count = word_count
        self.created_at = datetime.now()
        self.title = self._extract_title()
        self.audio_generated = False
        self.audio_path = None
    
    def _extract_title(self):
        """Extract title from the story text"""
        lines = self.text.strip().split('\n')
        
        # Check if the first line looks like a title
        if lines and len(lines[0]) < 100 and not lines[0].endswith('.'):
            return lines[0].strip()
        
        # Look for a line that starts with "Title:"
        for line in lines[:5]:  # Only check first 5 lines
            if line.lower().startswith('title:'):
                return line.split(':', 1)[1].strip()
                
        return "Bedtime Story"
    
    def to_dict(self):
        """Convert story to dictionary for serialization"""
        return {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'genre': self.genre,
            'age_group': self.age_group,
            'word_count': self.word_count,
            'created_at': self.created_at.isoformat(),
            'audio_generated': self.audio_generated,
            'audio_path': self.audio_path
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create a Story instance from dictionary data"""
        story = cls(
            id=data['id'],
            text=data['text'],
            genre=data['genre'],
            age_group=data.get('age_group', 'Unknown'),
            word_count=data['word_count']
        )
        
        if 'created_at' in data:
            try:
                story.created_at = datetime.fromisoformat(data['created_at'])
            except (ValueError, TypeError):
                pass
        
        if 'audio_generated' in data:
            story.audio_generated = data['audio_generated']
            
        if 'audio_path' in data:
            story.audio_path = data['audio_path']
            
        return story
    
    @classmethod
    def from_session(cls, session_data):
        """Create a Story instance from session data"""
        if not session_data:
            return None
            
        return cls.from_dict(session_data)


class StoryRepository:
    """
    Repository class for storing and retrieving stories
    
    Note: This is a simple in-memory repository.
    For persistence, this would be replaced with database operations.
    """
    
    def __init__(self):
        """Initialize an empty repository"""
        self.stories = {}
    
    def add(self, story):
        """Add a story to the repository"""
        self.stories[story.id] = story
        return story
    
    def get(self, story_id):
        """Get a story by ID"""
        return self.stories.get(story_id)
    
    def get_all(self):
        """Get all stories"""
        return list(self.stories.values())
    
    def delete(self, story_id):
        """Delete a story by ID"""
        if story_id in self.stories:
            del self.stories[story_id]
            return True
        return False