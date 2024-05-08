from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate
from langchain.chat_models.openai import ChatOpenAI
from langchain.schema import SystemMessage
from langchain.chains.llm import LLMChain

from entity.chat_model import ChatModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(version='0.1')

chat = ChatOpenAI()

@app.get('/hello')
def hello():
    return {"message": "Hello World"}

@app.post('/prompt')
def send_prompt(chat_model: ChatModel):
    presets = chat_model.presets or []
    messages=[(item.role, item.content) for item in presets]

    prompt = ChatPromptTemplate.from_messages(messages)
    prompt.append(HumanMessagePromptTemplate.from_template("{input}"))

    chain = prompt | chat
    
    result = chain.invoke({"input": chat_model.prompt})
    return result.content


