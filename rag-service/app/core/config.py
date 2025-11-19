#app/core/config.property
 
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    rabbitmq_user: str = "user"
    rabbitmq_password: str = "password"
    rabbitmq_host: str = "rabbitmq"
    rabbitmq_port: int = 5672
    rag_queue: str = "rag_queue"
    llm_queue: str = "llm_queue"

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "rag"

    logs_path: str | None = None
    file_log_level: str = "DEBUG"
    console_log_level: str = "INFO"

    openai_api_key: str
    openai_embeddings_model: str = "text-embedding-3-small"

    @property
    def rabbitmq_url(self) -> str:
        return F"amqp://{self.rabbitmq_user}:{self.rabbitmq_password}@{self.rabbitmq_host}:{self.rabbitmq_port}/"

    class Config:
        env_file = "app/.env"
        env_file_encoding = "utf-8"


settings = Settings()