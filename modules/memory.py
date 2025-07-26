from collections import defaultdict, deque
from modules.config import SHORT_TERM_HISTORY

# In-memory short-term memory (per session)
class ShortTermMemory:
    def __init__(self, max_history=SHORT_TERM_HISTORY):
        self.histories = defaultdict(lambda: deque(maxlen=max_history))

    def add(self, session_id, user, bot):
        self.histories[session_id].append({'user': user, 'bot': bot})

    def get(self, session_id):
        return list(self.histories[session_id]) 