from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    rabbitmq_user: str = "user"
    rabbitmq_password: str = "password"
    rabbitmq_host: str = "rabbitmq"
    rabbitmq_port: int = 5672
    upload_queue: str = "upload_queue"
    embedding_queue: str = "embedding_queue"
    chunk_size: int = 2000

    files_path: str = "/app/uploads/"
    logs_path: str | None = None
    file_log_level: str = "DEBUG"
    console_log_level: str = "INFO"

    @property
    def rabbitmq_url(self) -> str:
        return F"amqp://{self.rabbitmq_user}:{self.rabbitmq_password}@{self.rabbitmq_host}:{self.rabbitmq_port}/"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
