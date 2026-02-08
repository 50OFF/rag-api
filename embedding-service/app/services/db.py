#app/services/db.py

import asyncpg
from pgvector.asyncpg import register_vector
from asyncpg import exceptions

class DataBase():
    def __init__(self, host: str, port: int, user: str, password: str, db: str):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.pool = None

    async def connect(self):
        "Connect to database."
        self.pool =  await asyncpg.create_pool(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.db,
            init=register_vector
        )

    async def create_embeddings_table(self):
        "Create embeddings table."
        async with self.pool.acquire() as connection:
            await connection.execute(
                """
                CREATE TABLE IF NOT EXISTS embeddings (
                    chunk_id TEXT PRIMARY KEY,
                    file_id TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    text TEXT,
                    embedding vector(1536)
                );
                """
            )

    async def insert_embedding(self, chunk_id: str, file_id: str, user_id: str, text: str, embedding: list):
        "Insert new row in embeddings table."
        try:
            async with self.pool.acquire() as connection:
                await connection.execute(
                    """
                    INSERT INTO embeddings (chunk_id, file_id, user_id, text, embedding)
                    VALUES ($1, $2, $3, $4, $5)
                    """,
                    chunk_id, file_id, user_id, text, embedding
                )
        
        except exceptions.UndefinedTableError:
            await self.create_embeddings_table()

            async with self.pool.acquire() as connection:
                await connection.execute(
                    """
                    INSERT INTO embeddings (chunk_id, file_id, user_id, text, embedding)
                    VALUES ($1, $2, $3, $4, $5)
                    """,
                    chunk_id, file_id, user_id, text, embedding
                )
