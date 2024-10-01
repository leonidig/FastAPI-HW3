from fastapi import FastAPI
import uvicorn

app = FastAPI(debug=True)


from . import routes


def run() -> None:
    uvicorn.run(app, host="127.0.0.1", port=8000)

