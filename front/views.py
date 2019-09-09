from random import choice

import markdown
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, Count
from django.db.models.functions import ExtractYear, ExtractMonth
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView, Response

from admin.models import Article, Category, Comment, Like, User, Link, Site
from admin.page import FrontPagination, get_page_response
from admin.serializers import ArticleSerializers, CategorySerializers, CommentSerializers, UserSerializers
from celery_tasks.tasks import send_mail_task


# 获取随机字符串
def random_email_code(length):
    chars = '0123456789aceghimnsuw'
    random_str = []
    for i in range(length):
        random_str.append(choice(chars))
    return "".join(random_str)


# 获取所有主类列表
@api_view(['GET'])
def get_parent_sorts(request):
    parent_sorts = Category.objects.filter(is_parent=1).only('category_name')
    parent_sorts_ser = CategorySerializers(instance=parent_sorts, many=True)
    return Response({"parent": parent_sorts_ser.data})


# 根据parent_id获取所有次级分类列表
@api_view(['GET'])
def get_child_sorts(request):
    parent_id = request.GET['parent_id']
    parent = Category.objects.get(id=parent_id)
    child_sorts = Category.objects.filter(parent=parent)
    child_sorts_ser = CategorySerializers(instance=child_sorts, many=True)
    return Response(child_sorts_ser.data)


def index(request):
    try:
        admin_user = User.objects.values('user_img').get(user_authority=1)
    except User.DoesNotExist:
        admin_user = None
    like_list = Article.objects.values('id', 'title').filter(Q(is_like=1) & Q(is_show=1)).order_by("-gmt_created")[:8]
    # slide_list = Slide.objects.filter().order_by("-gmt_created")[:5]
    hot_articles = Article.objects.values('id', 'title').filter(is_show=1).order_by('-read_number')[:8]
    article_list = Article.objects.filter(is_show=1).defer('gmt_modified', 'remark').order_by('-gmt_created')
    paginator = Paginator(article_list, 6)  # 初始化分页对象，每页6条
    page = request.GET.get('page')  # 从GET请求中获取页码
    try:
        page_data = paginator.page(page)
    except PageNotAnInteger:
        page_data = paginator.page(1)  # 页码不是数字，跳到第一页
    except EmptyPage:
        page_data = paginator.page(paginator.num_pages)  # 页码超出范围，跳到最后一页
    context = {"admin_user": admin_user, "like_list": like_list, "hot_articles": hot_articles,
               "article_list": page_data}
    return render(request, 'index.html', context=context)


# 首页根据关键词——获取文章列表（分页）
class ArticleView(APIView):
    def get(self, request):
        category = request.GET.get('category')
        if category != '':
            article_list = Article.objects.filter(
                Q(category__category_name=category) | Q(category__parent__category_name=category),
                Q(is_show=1))
        else:
            article_list = Article.objects.filter(Q(is_show=1))
        article_list = article_list.order_by('-gmt_created')
        page = FrontPagination()
        page_articles = page.paginate_queryset(queryset=article_list, request=request, view=self)
        articles_ser = ArticleSerializers(instance=page_articles, many=True)
        return get_page_response(page, articles_ser.data)


# 登录页显示
def login_dis(request):
    return render(request, 'login.html')


# 注册页显示
def reg_dis(request):
    return render(request, 'reg.html')


# 文章详情页显示
def article_detail(request, article_id):
    user_id = request.session.get('user_id')
    article = Article.objects.get(id=article_id)
    article.read_number = article.read_number + 1
    article.save()
    # md = markdown.markdown(article.content.replace("\r\n", '  \n'), extensions=[
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    article.content = md.convert(article.content.replace("\r\n", '  \n'))
    prev_article = Article.objects.values('id', 'title').filter(id__lt=article_id).order_by('-id').first()
    next_article = Article.objects.values('id', 'title').filter(id__gt=article_id).order_by('id').first()
    comment_list = Comment.objects.filter(article_id=article_id).defer('gmt_modified', 'remark').order_by(
        "-gmt_created")
    for comment in comment_list:
        comment.content = md.convert(comment.content)
    like_list = Like.objects.filter(article_id=article_id, user_id=user_id).only('is_like', 'comment__id')
    like_id_list = Like.objects.values('id').filter(article_id=article_id, user_id=user_id).values_list('comment_id',
                                                                                                        flat=True)
    context = {"article": article, "like_list": like_list,
               "like_id_list": list(like_id_list), "prev_article": prev_article, "next_article": next_article,
               "comment_list": comment_list, 'toc': md.toc}
    return render(request, 'article-detail.html', context=context)


# 发表评论
@api_view(['POST'])
def publish_comment(request):
    try:
        user_name = request.session['user_name']
        comment = CommentSerializers(data=request.data)
        if comment.is_valid():
            # print(comment.validated_data)
            comment.save()
            json_data = {"msg": "评论成功", "code": 1}
        else:
            # print(comment.errors)
            json_data = {"msg": "评论失败", "code": 0}
    except KeyError:
        json_data = {"msg": "请先登录", "code": 0}
    return Response(json_data)


# 点赞评论
@api_view(['POST'])
def like_comment(request):
    try:
        user_name = request.session['user_name']
        comment_id = request.POST.get('comment_id')
        user_id = request.POST.get('user_id')
        comment = Comment.objects.get(id=comment_id)
        article_id = comment.article_id
        try:
            like = Like.objects.get(comment_id=comment_id, user_id=user_id)
            if like.is_like == 1:
                like.is_like = 0
                comment.liked_number = comment.liked_number - 1
            else:
                like.is_like = 1
                comment.liked_number = comment.liked_number + 1
        except Like.DoesNotExist:
            like = Like()
            like.is_like = 1
            like.user_id = user_id
            like.comment_id = comment_id
            like.article_id = article_id
            comment.liked_number = comment.liked_number + 1
        try:
            like.save()
            comment.save()
            json_data = {"msg": "点赞成功", "code": 1}
        except Exception as e:
            print(e)
            json_data = {"msg": "点赞失败", "code": 0}
    except KeyError:
        json_data = {"msg": "请先登录", "code": 0}
    return Response(json_data)


# 删除评论
@api_view(['GET'])
def delete_comment(request):
    id = request.GET.get('id')
    # print("id: " + str(id))
    try:
        comment = Comment.objects.get(id=id)
        article = Article.objects.get(id=comment.article_id)
        # 若是回复他人评论
        if comment.to_comment is not None:
            # 将回复评论总数减1
            to_comment = comment.to_comment
            if to_comment.reply_count > 0:
                to_comment.reply_count = to_comment.reply_count - 1
            to_comment.save()
        # 删除评论
        comment.delete()
        article.comment_number = Comment.objects.filter(article_id=comment.article_id).count()
        article.save()
        json_data = {"msg": "删除成功", "code": 1}
    except Exception as e:
        json_data = {"msg": "删除失败", "code": 0}
        print(e)
    return Response(json_data)


# 回复评论
@api_view(['POST'])
def reply_comment(request):
    try:
        user_name = request.session['user_name']
        comment = CommentSerializers(data=request.data)
        if comment.is_valid():
            comment.save()
            to_comment = Comment.objects.get(id=request.POST['to_comment_id'])
            to_comment.reply_count = to_comment.reply_count + 1
            to_comment.save()
            json_data = {"msg": "回复成功", "code": 1}
        else:
            json_data = {"msg": "回复失败", "code": 0}
    except KeyError:
        json_data = {"msg": "请先登录", "code": 0}
    return Response(json_data)


# 用户中心页面显示
def user_center_dis(request):
    # 已登录
    try:
        user_name = request.session['user_name']
        user = User.objects.get(user_name=user_name)
        return render(request, 'user_center.html', {"user": user})
    # 未登录
    except KeyError:
        return render(request, 'login.html')


# 用户管理模块
class UserView(APIView):
    # 修改用户信息
    def post(self, request, format=None):
        user = UserSerializers(User(), data=request.data)
        if user.is_valid():
            user.save()
            json_data = {"msg": "保存成功", "code": 1}
        else:
            # print(user.errors)
            json_data = {"msg": user.error_messages, "code": 0}
        return Response(json_data)


# 日期归档
def blog_archive(request, year, month):
    article_list = Article.objects.filter(gmt_created__year=year, gmt_created__month=month, is_show=1).defer(
        'gmt_modified', 'remark').order_by(
        '-gmt_created')
    paginator = Paginator(article_list, 5)  # 初始化分页对象，每页5条
    page = request.GET.get('page')  # 从GET请求中获取页码
    try:
        page_data = paginator.page(page)
    except PageNotAnInteger:
        page_data = paginator.page(1)  # 页码不是数字，跳到第一页
    except EmptyPage:
        page_data = paginator.page(paginator.num_pages)  # 页码超出范围，跳到最后一页
    # dates = Article.objects.datetimes('gmt_created', 'month', order='DESC').annotate(number=Count('id'))
    articles_all = Article.objects.filter()
    dates = articles_all.annotate(year=ExtractYear('gmt_created'), month=ExtractMonth('gmt_created')). \
        values('year', 'month').order_by('-year', '-month').annotate(number=Count('id'))
    context = {'article_list': page_data, 'dates': dates, 'year_search': int(year), 'month_search': int(month)}
    return render(request, 'blog-archive.html', context)


# 获取所有文章(归档)
def archive_all(request):
    article_list = Article.objects.filter(is_show=1).defer('gmt_modified', 'remark').order_by('-gmt_created')
    paginator = Paginator(article_list, 5)  # 初始化分页对象，每页5条
    page = request.GET.get('page')  # 从GET请求中获取页码
    try:
        page_data = paginator.page(page)
    except PageNotAnInteger:
        page_data = paginator.page(1)  # 页码不是数字，跳到第一页
    except EmptyPage:
        page_data = paginator.page(paginator.num_pages)  # 页码超出范围，跳到最后一页
    # dates = Article.objects.datetimes('gmt_created', 'month', order='DESC').annotate(number=Count('id'))
    articles_all = Article.objects.filter(is_show=1)
    dates = articles_all.annotate(year=ExtractYear('gmt_created'), month=ExtractMonth('gmt_created')). \
        values('year', 'month').order_by('-year', '-month').annotate(number=Count('id'))
    context = {'article_list': page_data, 'dates': dates}
    return render(request, 'blog-archive.html', context)


# 获取所有文章(标签墙)
def label_all(request):
    article_list = Article.objects.filter(is_show=1).defer('gmt_modified', 'remark').order_by('-gmt_created')
    paginator = Paginator(article_list, 5)  # 初始化分页对象，每页5条
    page = request.GET.get('page')  # 从GET请求中获取页码
    try:
        page_data = paginator.page(page)
    except PageNotAnInteger:
        page_data = paginator.page(1)  # 页码不是数字，跳到第一页
    except EmptyPage:
        page_data = paginator.page(paginator.num_pages)  # 页码超出范围，跳到最后一页
    label_list = Category.objects.filter(is_parent=0).annotate(number=Count('article')).order_by("-gmt_created")
    context = {'article_list': page_data, 'label_list': label_list}
    return render(request, 'label_wall.html', context)


# 标签墙
def label_wall(request, label):
    article_list = Article.objects.filter(category__category_name=label, is_show=1).defer('gmt_modified',
                                                                                          'remark').order_by(
        '-gmt_created')
    paginator = Paginator(article_list, 5)  # 初始化分页对象，每页5条
    page = request.GET.get('page')  # 从GET请求中获取页码
    try:
        page_data = paginator.page(page)
    except PageNotAnInteger:
        page_data = paginator.page(1)  # 页码不是数字，跳到第一页
    except EmptyPage:
        page_data = paginator.page(paginator.num_pages)  # 页码超出范围，跳到最后一页
    label_list = Category.objects.filter(is_parent=0).annotate(number=Count('article')).order_by("-gmt_created")
    context = {'article_list': page_data, 'label_list': label_list, 'label_name': label}
    return render(request, 'label_wall.html', context)


def search(request, key):
    article_list = Article.objects.filter(Q(title__icontains=key) | Q(user__user_name__icontains=key),
                                          Q(is_show=1)).defer('gmt_modified', 'remark').order_by(
        '-gmt_created')
    paginator = Paginator(article_list, 5)  # 初始化分页对象，每页5条
    page = request.GET.get('page')  # 从GET请求中获取页码
    try:
        page_data = paginator.page(page)
    except PageNotAnInteger:
        page_data = paginator.page(1)  # 页码不是数字，跳到第一页
    except EmptyPage:
        page_data = paginator.page(paginator.num_pages)  # 页码超出范围，跳到最后一页
    context = {'article_list': page_data}
    return render(request, 'search.html', context=context)


# 分类页面
def category_all(request):
    article_list = Article.objects.filter(is_show=1).order_by('-gmt_created')
    paginator = Paginator(article_list, 5)  # 初始化分页对象，每页5条
    page = request.GET.get('page')  # 从GET请求中获取页码
    try:
        page_data = paginator.page(page)
    except PageNotAnInteger:
        page_data = paginator.page(1)  # 页码不是数字，跳到第一页
    except EmptyPage:
        page_data = paginator.page(paginator.num_pages)  # 页码超出范围，跳到最后一页
    # category_list = Category.objects.filter(is_parent=0).annotate(number=Count('parent'))
    sql = "SELECT  mbc.id,mbc.category_name,COUNT(mba.title) AS number" \
          " FROM mb_category AS mbc " \
          " LEFT JOIN mb_category AS mbc_2 ON mbc.id = mbc_2.parent_id" \
          " LEFT JOIN mb_article AS mba ON mba.category_id = mbc_2.id" \
          " WHERE mbc.is_parent = 1" \
          " GROUP BY mbc_2.parent_id" \
          " ORDER BY mbc.gmt_created DESC;"
    cate_list = Category.objects.raw(sql)
    context = {'article_list': page_data, 'category_list': cate_list}
    return render(request, 'category.html', context)


# 分类筛选
def category(request, sort):
    article_list = Article.objects.filter(category__parent__category_name=sort,
                                          is_show=1).only('id', 'title', 'img', 'content',
                                                          'read_number', 'comment_number', 'gmt_created',
                                                          'category__parent__category_name',
                                                          'category__category_name', 'user__user_name').order_by(
        '-gmt_created')
    paginator = Paginator(article_list, 5)  # 初始化分页对象，每页5条
    page = request.GET.get('page')  # 从GET请求中获取页码
    try:
        page_data = paginator.page(page)
    except PageNotAnInteger:
        page_data = paginator.page(1)  # 页码不是数字，跳到第一页
    except EmptyPage:
        page_data = paginator.page(paginator.num_pages)  # 页码超出范围，跳到最后一页
    # category_list = Category.objects.filter(is_parent=0).annotate(number=Count('parent'))
    sql = "SELECT  mbc.id,mbc.category_name,COUNT(mba.title) AS number" \
          " FROM mb_category AS mbc " \
          " LEFT JOIN mb_category AS mbc_2 ON mbc.id = mbc_2.parent_id" \
          " LEFT JOIN mb_article AS mba ON mba.category_id = mbc_2.id" \
          " WHERE mbc.is_parent = 1" \
          " GROUP BY mbc_2.parent_id" \
          " ORDER BY mbc.gmt_created DESC;"
    cate_list = Category.objects.raw(sql)
    context = {'article_list': page_data, 'category_name': sort, 'category_list': cate_list}
    return render(request, 'category.html', context)


# 友情链接
def links(request):
    link_list = Link.objects.filter().only('link_name', 'link_url', 'description')
    return render(request, 'links.html', {"link_list": link_list})


# 拦截器跳转
def response(request, error):
    return render(request, 'login.html', {'error': error})


# 发送验证邮件
@api_view(['GET'])
def send_reg_email(request):
    to_email = request.GET.get('to_email')
    print("to_email: " + to_email)
    try:
        email_code = request.session['email_code']
    except KeyError:
        email_code = random_email_code(4)
        request.session['email_code'] = email_code
        request.session.set_expiry(600)
    site_name = "Shadow Blog"
    site = Site.objects.values('site_name').filter().first()
    if site:
        site_name = site.site_name
    msg = "【" + site_name + "】 您的验证码为" + email_code + "（10分钟内有效），为了保证您的账户安全，" \
                                                      "请勿向他人提供此验证码。感谢光临" + site_name + "!"
    try:
        send_mail_task.delay(site_name, to_email, msg)  # 使用delay调用任务
        json_data = {'msg': '验证码已发送', "code": 1}
    except Exception as e:
        print(e)
        json_data = {'msg': '验证码发送失败', "code": 0}
    return Response(json_data)
