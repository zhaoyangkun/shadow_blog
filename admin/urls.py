from django.urls import path
from admin import views

urlpatterns = [
    path('', views.to_admin_index, name='adminIndex'),  # 后台主页显示
    path('code', views.get_verify_img, name='code'),  # 验证码
    path('welcome', views.to_welcome, name='welcome'),  # 显示欢迎界面

    path('login', views.LoginView.as_view(), name='login'),  # 登录API
    path('register', views.RegisterView.as_view(), name='register'),  # 注册API

    path('userDis', views.user_dis, name='userDis'),  # 用户管理页面显示
    path('userEditDis/<int:user_id>/', views.edit_pwd_dis, name='userEditDis'),  # 用户管理模块
    path('user', views.UserView.as_view(), name='user'),  # 用户管理模块

    path('sortDis', views.sort_dis, name='sortDis'),  # 显示分类页面
    path('parentSorts', views.get_parent_sorts, name='parentSorts'),  # 获取所有主类列表
    path('getChildSorts', views.get_child_sorts, name='getChildSorts'),  # 根据parent_id获取所有次级分类列表
    path('sortAddDis', views.sort_add_dis, name='sortAddDis'),  # 显示添加分类页面
    path('sortEditDis/<int:id>/', views.sort_eidt_dis, name='sortEditDis'),  # 显示修改分类页面
    path('sort', views.SortView.as_view(), name='sort'),  # 文章分类管理模块
    path('labelDis', views.label_dis, name='labelDis'),  # 标签管理页显示
    path('labelAddDis', views.label_add_dis, name='labelAddDis'),  # 添加标签页显示
    path('labelEditDis/<int:id>/', views.label_edit_dis, name='labelEditDis'),  # 修改标签页显示

    path('articleDis', views.article_dis, name='articleDis'),  # 文章列表页显示
    path('articleAddDis', views.add_article_dis, name='articleAddDis'),  # 添加文章页面显示
    path('articleEditDis/<int:id>/', views.edit_article_dis, name='articleEditDis'),  # 编辑文章页面显示
    path('article', views.ArticleView.as_view(), name='article'),  # 文章管理模块

    path('slideDis', views.to_slide, name='slideDis'),  # 显示轮播列表页面
    path('slideAddDis', views.add_slide_dis, name='slideAddDis'),  # 显示添加轮播页面
    path('slideEditDis/<int:id>/', views.edit_slide_dis, name='slideEditDis'),  # 显示修改轮播页面
    path('slide', views.SlideView.as_view(), name='slide'),  # 轮播API

    path('commentListDis', views.to_comment_list, name='commentListDis'),  # 显示评论列表页面
    path('comment', views.CommentView.as_view(), name='comment'),  # 评论API

    path('linkDis', views.links_dis, name='linkDis'),  # 显示轮播列表页面
    path('linkAddDis', views.link_add_dis, name='linkAddDis'),  # 显示添加轮播页面
    path('linkEditDis/<int:id>/', views.link_edit_dis, name='linkEditDis'),  # 显示修改轮播页面
    path('link', views.LinkView.as_view(), name='link'),  # 轮播API
    path('delete_links', views.delete_checked_links, name='delete_links'),  # 批量删除友链

    path('site_setting_dis', views.site_setting_dis, name='site_setting_dis'),  # 站点设置
    path('site_api', views.SiteView.as_view(), name='site_api'),  # 站点API
]
