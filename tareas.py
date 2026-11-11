import time
import random
from celery import Celery
from celery.exceptions import SoftTimeLimitExceeded

celery_app = Celery(
    "tareas",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
)

celery_app.conf.update(
    task_track_started=True,
    result_expires=3600,
)


def llamar_pasarela_bancaria():
    """Simula el comportamiento de un banco real muy inestable"""
    time.sleep(random.uniform(1, 4))   
    if random.random() < 0.3:          
        raise Exception("Error 504: El banco no responde")
    return "Pago Aprobado"


@celery_app.task(bind=True, max_retries=3, soft_time_limit=5)
def procesar_pago(self):
    try:
        return llamar_pasarela_bancaria()
    except SoftTimeLimitExceeded:
        raise Exception("Tiempo límite excedido (5s)")
    except Exception as exc:
        raise self.retry(exc=exc, countdown=2)