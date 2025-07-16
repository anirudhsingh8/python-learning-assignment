from fastapi import FastAPI
from starlette import status

app = FastAPI()

@app.get('/health', status_code=status.HTTP_200_OK)
def check_health():
    return {'message': 'OK'}