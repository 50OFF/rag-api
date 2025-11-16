from fastapi import FastAPI, UploadFile, File
from app.services.rabbitmq_client import RabbitMQClient
from app.core.config import settings
import uuid
import os

app = FastAPI()
rabbitmq_client = RabbitMQClient(settings.rabbitmq_url)

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

    with open(file_url, "wb") as f:
        f.write(await file.read())

    await rabbitmq_client.publish_message(settings.upload_queue, {"file_id": file_id,
                                                                  "user_id": '123',
                                                                  "file_url": file_url})
    return {"message": "upload"}

@app.post("/rag")
async def rag():
    await rabbitmq_client.publish_message(settings.rag_queue, {"message": "rag"})
    return {"message": "rag"}

@app.get("/llm")
async def llm():
    await rabbitmq_client.publish_message(settings.llm_queue, {"message": "llm"})
    return {"message": "llm"}