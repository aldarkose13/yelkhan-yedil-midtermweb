from fastapi import FastAPI

from app.database import Base, engine
from app.routers import criminals, hunts

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Space Bounty Hunters API")
app.include_router(criminals.router)
app.include_router(hunts.router)
