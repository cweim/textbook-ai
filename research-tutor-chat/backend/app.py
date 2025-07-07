from fastapi import FastAPI, Request
from tutor_api import get_tutor_response

app = FastAPI()

@app.post("/tutor")
async def tutor_endpoint(req: Request):
    data = await req.json()
    query = data.get("query")
    result = get_tutor_response(query)
    return result
