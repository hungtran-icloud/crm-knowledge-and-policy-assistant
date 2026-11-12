"""Celery tasks for async batch processing — import-service."""
import os
from celery import Celery

from src.importer.engine import DataImportEngine
from src.importer.models import BatchType

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

app = Celery("import_tasks", broker=REDIS_URL, backend=REDIS_URL)
app.conf.task_routes = {"src.tasks.*": {"queue": "import_queue"}}
app.conf.task_serializer = "json"
app.conf.result_serializer = "json"
app.conf.accept_content = ["json"]


@app.task(name="src.tasks.process_passages_batch")
def process_passages_batch(file_path: str, batch_type: str = "snapshot", force: bool = False):
    engine = DataImportEngine()
    b_type = BatchType.SNAPSHOT if batch_type == "snapshot" else BatchType.INCREMENT
    manifest = engine.import_passages(file_path, batch_type=b_type, force=force)
    return manifest.to_dict()


@app.task(name="src.tasks.process_critical_fields_batch")
def process_critical_fields_batch(file_path: str, batch_type: str = "snapshot", force: bool = False):
    engine = DataImportEngine()
    b_type = BatchType.SNAPSHOT if batch_type == "snapshot" else BatchType.INCREMENT
    manifest = engine.import_critical_fields(file_path, batch_type=b_type, force=force)
    return manifest.to_dict()


@app.task(name="src.tasks.process_crm_context_batch")
def process_crm_context_batch(file_path: str, batch_type: str = "snapshot", force: bool = False):
    engine = DataImportEngine()
    b_type = BatchType.SNAPSHOT if batch_type == "snapshot" else BatchType.INCREMENT
    manifest = engine.import_crm_context(file_path, batch_type=b_type, force=force)
    return manifest.to_dict()
