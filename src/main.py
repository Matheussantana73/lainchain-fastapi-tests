from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate

from entity.chat_model import ChatModel
from dotenv import load_dotenv

from operations.build_chat_model_llm_chain import ChatModelLLMChain

load_dotenv()

app = FastAPI(version='0.1')

@app.get('/hello')
def hello():
    return {"message": "Hello World"}

@app.post('/prompt')
def send_prompt(chat_model: ChatModel):
    llm = ChatModelLLMChain(chat_model=chat_model).build()

    prompt = chat_model_to_chat_prompt(chat_model)
    prompt.append(HumanMessagePromptTemplate.from_template("{input}"))

    chain = prompt | llm

    result = chain.invoke({"input": chat_model.prompt})
    return result.content


def chat_model_to_chat_prompt(chat_model: ChatModel):
    presets = chat_model.presets or []
    messages=[(item.role, item.content) for item in presets]
    return ChatPromptTemplate.from_messages(messages)

