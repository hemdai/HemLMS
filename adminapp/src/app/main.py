from fastapi import FastAPI
from src.app import admin_router

app = FastAPI(
    title="HemLMSADMIN", version="1.0.0", swagger_ui_parameters={"tagsSorter": "alpha"}
)
API_V1 = "/api/v1"

app.include_router(router=admin_router, prefix="/api/v1")
