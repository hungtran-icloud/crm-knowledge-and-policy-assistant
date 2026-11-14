"""Celery application — background jobs for import, indexing, evaluation."""
from celery import Celery
import os

app = Celery(
    "ckpa-worker",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/1"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/2"),
    include=["src.tasks.import_task", "src.tasks.index_task", "src.tasks.eval_task"],
)

app.conf.beat_schedule = {
    # Chạy snapshot staleness check mỗi giờ
    "check-snapshot-staleness": {
        "task": "src.tasks.import_task.check_staleness",
        "schedule": 3600.0,
    },
}
