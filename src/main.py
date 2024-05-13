from fastapi import FastAPI, HTTPException
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from openai import AuthenticationError
from pydantic.v1.error_wrappers import ValidationError

from entity.chat_model import ChatModel

from operations.build_chat_model_llm_chain import ChatModelLLMChain

app = FastAPI(version='0.1')

@app.get('/hello')
def hello():
    return {"message": "Hello World"}

@app.post('/prompt')
def send_prompt(chat_model: ChatModel):
    try:
        llm = ChatModelLLMChain(chat_model=chat_model).build()

        prompt = chat_model_to_chat_prompt(chat_model)
        prompt.append(HumanMessagePromptTemplate.from_template("{input}"))

        chain = prompt | llm

        result = chain.invoke({"input": chat_model.prompt})
        return result.content
    except AuthenticationError as e:
        response = e.response
        data = response.json()
        raise HTTPException(
            detail=data, status_code=response.status_code
        ) from e
    except ValidationError as e:
        raise HTTPException(
            detail=e.errors(),
            status_code=422
        ) from e
    except Exception as e:
        raise HTTPException(
            detail=e.args,
            status_code=422
        ) from e



def chat_model_to_chat_prompt(chat_model: ChatModel):
    presets = chat_model.presets or []
    messages=[(item.role, item.content) for item in presets]
    return ChatPromptTemplate.from_messages(messages)

