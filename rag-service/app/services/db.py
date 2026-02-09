#app/services/db.py

import asyncpg
from asyncpg import Pool, Record
from pgvector.asyncpg import register_vector
from typing import Any

class DataBase():
    def __init__(self, host: str, port: int, user: str, password: str, db: str):
        self.host: str = host
        self.port: int = port
        self.user: str = user
        self.password: str = password
        self.db: str = db
        self.pool: Pool | None  = None

    async def connect(self):
        "Connect to database."
        self.pool = await asyncpg.create_pool(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.db,
            init=register_vector
        )
    
    async def ensure_connection(self):
        "Ensure database connection"
        if self.pool is None:
            await self.connect()

    async def query(self, sql: str, *args: Any) -> list[Record] | None:
        "Database SQL query."
        await self.ensure_connection()

        sql_low = sql.strip().lower()

        async with self.pool.acquire() as conn:
            if sql_low.startswith("select"):
                return await conn.fetch(sql, *args)

            if "returning" in sql_low:
                return await conn.fetchrow(sql, *args)

            else:
                return await conn.execute(sql, *args)
    
    async def close(self):
        if self.pool:
            await self.pool.close()
