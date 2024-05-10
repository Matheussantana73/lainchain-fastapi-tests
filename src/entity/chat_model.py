from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

class LLMModel(str, Enum):
    openai = 'ChatGPT'
    ollama = 'ChatOllama'


class RoleItemChatModel(str, Enum):
    human = 'human'
    ai = 'ai'
    system = 'system'

class ItemChatModel(BaseModel):
    role: RoleItemChatModel
    content: str

class ChatModel(BaseModel):
    api_key: str
    llm: LLMModel = LLMModel.openai

    model: str = 'gpt-3.5-turbo'
    presets: Optional[List[ItemChatModel]] = []
    prompt: str

    temperature: int = 1
    max_tokens: int = 256
    top_p: int = 1
