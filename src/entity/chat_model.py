from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

class RoleItemChatModel(str, Enum):
    human = 'human'
    ai = 'ai'
    system = 'system'

class ItemChatModel(BaseModel):
    role: RoleItemChatModel
    content: str

class ChatModel(BaseModel):
    presets: Optional[List[ItemChatModel]] = []
    prompt: str

