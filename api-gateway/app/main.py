from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from contextlib import asynccontextmanager
from app.core.broker import RabbitMQClient
from app.core.config import settings
import uuid
import os

rabbit = RabbitMQClient(settings.rabbitmq_url)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ---------- Startup ----------
    # logger.info("Starting API service...")

    os.makedirs(settings.uploads_path, exist_ok=True)
    # logger.info(f"Uploads directory ensured: {settings.uploads_path}")

    # logger.info("Connecting to RabbitMQ...")
    await rabbit.connect()
    # logger.info("RabbitMQ connected.")

    yield  # <-- Application runs here

    # ---------- Shutdown ----------
    # logger.info("Shutting down API service...")
    if rabbit.connection:
        await rabbit.connection.close()
        # logger.info("RabbitMQ connection closed.")

app = FastAPI(lifespan=lifespan)

class RagRequest(BaseModel):
    question: str
    top_k: int

@app.get("/health")
async def check_health():
    return {"message": "ok"}

@app.post("/auth")
async def auth():
    return {"message" "auth"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())

    os.makedirs(settings.uploads_path, exist_ok=True)
    file_url = settings.uploads_path + f"/{file_id}_{file.filename}"
    file_name = f"{file_id}_{file.filename}"

    with open(file_url, "wb") as f:
        f.write(await file.read())

    await rabbit.produce(settings.upload_queue, {"file_id": file_id,
                                                "user_id": '123',
                                                "file_name": file_name})
    return {"message": "upload"}

@app.post("/rag/query")
async def rag(req: RagRequest):
    await rabbit.produce(settings.rag_queue, {"question": req.question,
                                              "top_k": req.top_k,
                                              "user_id": '123'})
    return {"message": "rag"}

@app.get("/llm")
async def llm():
    await rabbit.produce(settings.llm_queue, {"message": "llm"})
    return {"message": "llm"}
