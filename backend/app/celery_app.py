from celery import Celery

celery = Celery(
    "tg_publisher",
<<<<<<< HEAD
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/1"
)
=======
    broker="redis://tg_redis:6379/0",
    backend="redis://tg_redis:6379/1"
)

>>>>>>> abd87a6c29e9f56783cac546c133769c128e472a
celery.conf.update(
    task_routes={
        "tasks.publish_post_task": {"queue": "tg_publish"},
        "tasks.schedule_published_posts": {"queue": "tg_publish"},
    },
<<<<<<< HEAD
    timezone="UTC",
    enable_utc=True,
=======
    timezone="Europe/Kyiv",  # Киевский часовой пояс
    enable_utc=False,        # Выключаем UTC, чтобы использовать локальную зону
>>>>>>> abd87a6c29e9f56783cac546c133769c128e472a
    beat_schedule={
        'publish-scheduled-posts-every-minute': {
            'task': 'tasks.schedule_published_posts',
            'schedule': 60.0,
        },
    }
)
