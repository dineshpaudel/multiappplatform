from datetime import datetime

class Message:
    """
    Model class for a generated flirty message
    
    Note: This is a simple in-memory model.
    For persistence, this would be replaced with a database model.
    """
    
    def __init__(self, id, text, parameters):
        """
        Initialize a new Message instance
        
        Args:
            id (str): Unique identifier for the message
            text (str): The generated message text
            parameters (dict): The parameters used to generate the message
        """
        self.id = id
        self.text = text
        self.parameters = parameters
        self.created_at = datetime.now()
    
    def to_dict(self):
        """Convert message to dictionary for serialization"""
        return {
            'id': self.id,
            'text': self.text,
            'parameters': self.parameters,
            'created_at': self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create a Message instance from dictionary data"""
        message = cls(
            id=data['id'],
            text=data['text'],
            parameters=data['parameters']
        )
        
        if 'created_at' in data:
            try:
                message.created_at = datetime.fromisoformat(data['created_at'])
            except (ValueError, TypeError):
                pass
            
        return message


class MessageHistory:
    """
    Class for storing message generation history
    
    Note: This is a simple in-memory history.
    For persistence, this would be replaced with database operations.
    """
    
    def __init__(self, max_size=20):
        """
        Initialize an empty message history
        
        Args:
            max_size (int): Maximum number of messages to store in history
        """
        self.messages = []
        self.max_size = max_size
    
    def add(self, message):
        """
        Add a message to the history
        
        Args:
            message (Message): The message to add
            
        Returns:
            Message: The added message
        """
        self.messages.append(message)
        
        # Trim history if it exceeds max size
        if len(self.messages) > self.max_size:
            self.messages = self.messages[-self.max_size:]
            
        return message
    
    def get_all(self):
        """
        Get all messages from history
        
        Returns:
            list: List of Message objects
        """
        return self.messages
    
    def clear(self):
        """Clear the message history"""
        self.messages = []