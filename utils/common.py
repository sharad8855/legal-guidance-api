from collections import deque
from config import settings

class ConversationMemory:
    """Manages conversation history for LLM interactions."""
    
    def __init__(self, max_length=settings.MAX_CONVERSATION_HISTORY):
        self.memory = deque(maxlen=max_length)
    
    def add_user_message(self, message: str):
        """Add a user message to the conversation history."""
        self.memory.append({"role": "user", "content": message})
    
    def add_assistant_message(self, message: str):
        """Add an assistant message to the conversation history."""
        self.memory.append({"role": "assistant", "content": message})
    
    def get_conversation_context(self) -> str:
        """Get formatted conversation history for context."""
        return "\n".join([
            f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
            for msg in self.memory
        ])
    
    def clear(self):
        """Clear conversation history."""
        self.memory.clear()

# Create global conversation memory instance
conversation_memory = ConversationMemory()
