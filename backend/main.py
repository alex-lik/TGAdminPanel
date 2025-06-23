from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from database import Base, engine
import models
from config import LOG_PATH
from routes import groups, channels, posts

# Логирование
logger.add(LOG_PATH, rotation='1 day', retention='30 days')

# Создание таблиц (если их нет)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Telegram Content Manager", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(groups.router, prefix="/channel-groups", tags=["Channel Groups"])
app.include_router(channels.router, prefix="/channel-groups", tags=["Channels"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])

@app.get("/")
def root():
    return {"message": "Telegram Content Manager API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
