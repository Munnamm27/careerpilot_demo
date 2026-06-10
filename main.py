from fastapi import FastAPI
from routes.api import router

app = FastAPI(title="CareerPilot API")

@app.get('/')
def test():
    return "Hello"

app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)