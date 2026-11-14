"""Background tasks: vector indexing after publication."""
from src.celery_app import app


@app.task(name="src.tasks.index_task.index_passages")
def index_passages(document_version_id: str):
    # TODO: generate embeddings, upsert to pgvector
    pass


@app.task(name="src.tasks.index_task.withdraw_passages")
def withdraw_passages(document_version_id: str):
    # TODO: mark passages as withdrawn; block from retrieval
    pass
