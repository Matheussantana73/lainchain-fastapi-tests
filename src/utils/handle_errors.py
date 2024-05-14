
from functools import wraps
from typing import Any, Callable
from fastapi import HTTPException
from openai import AuthenticationError
from pydantic import ValidationError


def handler_llm_except(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            print('wrapper')
            return func(*args, **kwargs)
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
    return wrapper
