import json

def format_return(res):
    try:
        return json.loads(res)
    except Exception:
        return res

