from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="HemLMS", version="1.0.0", swagger_ui_parameters={"tagsSorter": "alpha"}
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from src.app import account_router, course_router

app.include_router(router=account_router, prefix="/api/v1")
app.include_router(router=course_router, prefix="/api/v1")
