#app/services/search.py

from app.services.embedder import Embedder
from app.services.db import DataBase
from app.models.events import RagEvent
from app.models.chunks import Chunk

async def rag_search(embedder: Embedder, db: DataBase, event: RagEvent) -> list[Chunk] | None:
    "Vector search."
    question = event.question
    user_id = event.user_id
    top_k = event.top_k

    question_embedding = await embedder.embed(question)

    rows = await db.query(
        """
        SELECT chunk_id, text, 1 - (embedding <=> $1) AS score
        FROM embeddings
        WHERE user_id = $2
        ORDER BY embedding <=> $1
        LIMIT $3;
        """,
        question_embedding,
        user_id,
        top_k
    )
    
    if rows is not None:
        chunks = []
        for row in rows:
            chunk_dict = {
                "id": str(row["chunk_id"]),
                "text": row["text"],
                "score": float(row["score"])
            }
            chunk = Chunk(**chunk_dict)
            chunks.append(chunk)
        return chunks
    else:
        return None
    