"""Background tasks: run evaluation sets, record metrics."""
from src.celery_app import app


@app.task(name="src.tasks.eval_task.run_evaluation")
def run_evaluation(eval_run_id: str):
    # TODO: run evaluation suite, record precision/recall/citation metrics
    pass
