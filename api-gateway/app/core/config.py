from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    rabbitmq_user: str = "user"
    rabbitmq_password: str = "password"
    rabbitmq_host: str = "rabbitmq"
    rabbitmq_port: int = 5672
    upload_queue: str = "upload_queue"
    rag_queue: str = "rag_queue"
    llm_queue: str = "llm_queue"
    uploads_path: str = "/tmp"

    @property
    def rabbitmq_url(self) -> str:
        return f"amqp://{self.rabbitmq_user}:{self.rabbitmq_password}@{self.rabbitmq_host}:{self.rabbitmq_port}/"
    
    class Config:
        env_file = "app/.env"
        env_file_encoding = "utf-8"


settings = Settings()