from django.urls import path

from front import views

# app_name = "front"

urlpatterns = [
    path('index', views.index, name='frontIndex'),  # 前台主页显示
    path('front_article', views.ArticleView.as_view(), name='front_article'),  # 首页根据关键词——获取文章列表（分页）
    path('loginDis', views.login_dis, name='loginDis'),  # 登录页显示
    path('regDis', views.reg_dis, name='regDis'),  # 注册页显示
    path('articleDetail/<int:article_id>/', views.article_detail, name='articleDetail'),  # 文章详情页显示
    # path('getChildCategory', views.get_child_sorts, name='getChildCategory'),  # 获取子集分类列表
    path('getParentCategory', views.get_parent_sorts, name='getParentCategory'),  # 获取父级分类列表
    path('publishComment', views.publish_comment, name='publishComment'),  # 发表评论
    path('replyComment', views.reply_comment, name='replyComment'),  # 回复评论
    path('likeComment', views.like_comment, name='likeComment'),  # 点赞评论
    path('deleteComment', views.delete_comment, name='deleteComment'),  # 点赞评论
    path('userCenter', views.user_center_dis, name='userCenterDis'),  # 个人中心页面显示
    path('userApi', views.UserView.as_view(), name='userApi'),  # 用户API
    path('archive/<str:year>/<str:month>/', views.blog_archive, name='archive'),  # 博客按年月归档
    path('archive', views.archive_all, name='archive_all'),
    path('label', views.label_all, name='label_wall_all'),
    path('label/<str:label>/', views.label_wall, name='label_wall'),  # 根据标签获取文章列表
    path('search/<str:key>/', views.search, name='search'),  # 关键字搜索
    path('category', views.category_all, name='category_all'),  # 文章分类页面
    path('category/<str:sort>/', views.category, name='category'),  # 文章分类筛选
    path('link', views.links, name='links'),  # 友情链接
    path('response/<str:error>/', views.response, name='response'),  # 拦截器跳转
    path('send_email', views.send_reg_email, name='send_email'),  # 发送邮箱注册码
]
