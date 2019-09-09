"""shadow_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from django.urls import include, re_path
from django.urls import path
from django.views.generic import TemplateView
from django.views.static import serve

from front import views
from shadow_blog.sitemap import ArticleSitemap
from shadow_blog.views import to_403_html, to_404_html, to_500_html

sitemaps = {
    'blog': ArticleSitemap,
}

urlpatterns = [
    # 主页显示
    path('', views.index, name='index'),

    # 前端
    path('front/', include('front.urls'), name='front'),

    # 后台
    path('admin/', include('admin.urls'), name='admin'),

    # veditor
    path('vditor/', include('vditor.urls'), name='vditor'),

    # oauth
    path('oauth/', include('oauth.urls')),

    # robots.txt
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),

    # sitemaps
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),  # media配置
]

# 错误页面
handler403 = to_403_html
handler404 = to_404_html
handler500 = to_500_html
