from celery_tasks.celery import app  # 导入创建好的celery应用
from django.core.mail import send_mail  # 使用django内置函数发送邮件
from django.conf import settings  # 导入django的配置


# bind：保证task对象会作为第一个参数自动传入
# name：异步任务别名
# retry_backoff：异常自动重试的时间间隔 第n次(retry_backoff×2^(n-1))s


@app.task
def send_mail_task(title, email, msg):
    """
    进入项目根目录执行命令行：celery -A celery_tasks worker -l info -P eventlet
    """
    # 使用django内置函数发送邮件
    send_mail(title, '', settings.DEFAULT_FROM_EMAIL, [email], html_message=msg)
