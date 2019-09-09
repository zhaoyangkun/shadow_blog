from django.urls import path

from vditor import views

urlpatterns = [
    # 上传图片
    path('img_upload', views.img_upload, name='img_upload'),
]
