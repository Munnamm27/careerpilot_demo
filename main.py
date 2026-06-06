from fastapi import FastAPI
from routes.api import router

app = FastAPI(title="CareerPilot API")
app.include_router(router)
