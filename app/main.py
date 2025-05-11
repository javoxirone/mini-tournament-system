from typing import Union

from fastapi import FastAPI

from app.api.tournament import router as tournament_router

app = FastAPI()


app.include_router(tournament_router)