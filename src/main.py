from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate

from entity.chat_model import ChatModel

from operations.build_chat_model_llm_chain import ChatModelLLMChain
from utils.handle_errors import handler_llm_except
from utils.helper import format_return

app = FastAPI(version='0.1')

@app.get('/hello')
def hello():
    return {"message": "Hello World"}

@app.post('/prompt')
@handler_llm_except
def send_prompt(chat_model: ChatModel):
    chain = build_llm_chain(chat_model)

    result = chain.invoke({"input": chat_model.prompt})
    return format_return(result.content)

def build_llm_chain(chat_model):
    llm = ChatModelLLMChain(chat_model=chat_model).build()

    prompt = chat_model_to_chat_prompt(chat_model)
    prompt.append(HumanMessagePromptTemplate.from_template("{input}"))

    return prompt | llm


def chat_model_to_chat_prompt(chat_model: ChatModel):
    presets = chat_model.presets or []
    messages=[(item.role, item.content) for item in presets]
    return ChatPromptTemplate.from_messages(messages)
