#app/services/search.py

from app.services.embedder import Embedder
from app.services.db import DataBase
from app.models.events import RagEvent

async def rag_search(embedder: Embedder, db: DataBase, event: RagEvent) -> list[dict] | None:
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
        return [
            {
                "id": str(r["chunk_id"]),
                "text": r["text"],
                "score": float(r["score"])
            }
            for r in rows
        ]
    else:
        return None
    