import os

from celery import Celery

from celery_tasks import celeryconfig  # 导入celery配置文件

# 为celery设置环境变量
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shadow_blog.settings")

# 创建celery app
app = Celery('celery_tasks')

# 从单独的配置模块中加载配置
app.config_from_object(celeryconfig)

# 设置app自动加载任务
app.autodiscover_tasks(['celery_tasks'])
