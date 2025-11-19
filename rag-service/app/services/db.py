#app/services/db.py

import asyncpg
from pgvector.asyncpg import register_vector

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

    async def query(self, sql: str, *args):
        if not sql:
            return None
        
        sql_low = sql.strip().lower()

        async with self.pool.acquire() as conn:
            if sql_low.startswith("select"):
                return await conn.fetch(sql, *args)

            if "returning" in sql_low:
                return await conn.fetchrow(sql, *args)

            else:
                return await conn.execute(sql, *args)