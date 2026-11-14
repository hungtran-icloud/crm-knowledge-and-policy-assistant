"""Background tasks: batch import, snapshot staleness check."""
from src.celery_app import app


@app.task(name="src.tasks.import_task.run_batch_import")
def run_batch_import(file_path: str, schema: str, batch_type: str = "snapshot"):
    # TODO: invoke DataImportEngine
    pass


@app.task(name="src.tasks.import_task.check_staleness")
def check_staleness():
    # TODO: check if latest snapshot is stale; alert if so
    pass
