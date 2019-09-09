from django.urls import path

from oauth import views

app_name = 'oauth'

urlpatterns = [
    path('github_login', views.github_login, name='github_login'),  # 调起github授权登录
    path('github_check', views.github_check, name='github_check'),  # github授权登录回调
    path('github_response/<str:info>/', views.github_response, name='github_response')  # 授权信息提示
]
