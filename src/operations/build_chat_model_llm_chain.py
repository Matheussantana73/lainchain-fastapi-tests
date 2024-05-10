
from langchain.chains.base import Chain
from langchain.chat_models.openai import ChatOpenAI
from langchain.chat_models.ollama import ChatOllama

from entity.chat_model import ChatModel, LLMModel


class ChatModelLLMChain:
    _KLASS_INSTANCIES: dict[LLMModel, Chain] = {
      'ChatGPT':  ChatOpenAI,
      'ChatOllama': ChatOllama
    }

    def __init__(self, chat_model: ChatModel) -> None:
        self.chat_model = chat_model

    def build(self) -> Chain:
        chat_model = self.chat_model
        klass = self._KLASS_INSTANCIES[chat_model.llm]

        return klass(
                api_key=chat_model.api_key,
                model=chat_model.model,
                temperature=chat_model.temperature,
                max_tokens=chat_model.max_tokens,
                top_p=chat_model.top_p,
            )
