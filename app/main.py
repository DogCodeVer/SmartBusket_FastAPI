from fastapi import FastAPI
from app.api.v1.endpoints import parser

app = FastAPI(title="Food Product Parser")

app.include_router(parser.router)
