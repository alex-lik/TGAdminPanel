from celery import Celery

celery = Celery(
    "tg_publisher",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/1"
)
celery.conf.update(
    task_routes={
        "tasks.publish_post_task": {"queue": "tg_publish"},
        "tasks.schedule_published_posts": {"queue": "tg_publish"},
    },
    timezone="UTC",
    enable_utc=True,
    beat_schedule={
        'publish-scheduled-posts-every-minute': {
            'task': 'tasks.schedule_published_posts',
            'schedule': 60.0,
        },
    }
)
