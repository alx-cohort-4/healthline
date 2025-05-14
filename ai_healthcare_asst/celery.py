from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_healthcare_asst.settings')
celery_app = Celery('ai_healthcare_asst')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.broker_connection('redis://localhost:6380/0')
celery_app.autodiscover_tasks()


@celery_app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
