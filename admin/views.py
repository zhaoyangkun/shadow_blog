import datetime
import io
import random

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import QueryDict
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.views import Response

from admin.models import User, Category, Article, Slide, Comment, Link, Site
from admin.page import StandardPagination, FrontPagination, get_page_response
from admin.serializers import UserSerializers, CategorySerializers, ArticleSerializers, SlideSerializers, \
    CommentSerializers, LinkSerializers, SiteSerializers


# Create your views here.

# 获取随机颜色
def get_random_color():
    R = random.randrange(255)
    G = random.randrange(255)
    B = random.randrange(255)
    return (R, G, B)


# 生成验证码
def get_verify_img(request):
    # 定义画布背景颜色
    bg_color = get_random_color()
    # 画布大小
    img_size = (200, 40)
    # 定义画布
    image = Image.new("RGB", img_size, bg_color)
    # 定义画笔
    draw = ImageDraw.Draw(image, "RGB")
    # 创建字体（字体的路径，服务器路径）
    font_path = 'static/img/DejaVuSans.ttf'
    # 实例化字体，设置大小是30
    font = ImageFont.truetype(font_path, 30)
    # 准备画布上的字符集
    source = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789"
    # 保存每次随机出来的字符
    code_str = ""
    for i in range(4):
        # 获取数字随机颜色
        text_color = get_random_color()
        # 获取随机数字 len
        tmp_num = random.randrange(len(source))
        # 获取随机字符 画布上的字符集
        random_str = source[tmp_num]
        # 将每次随机的字符保存（遍历） 随机四次
        code_str += random_str
        # 将字符画到画布上
        draw.text((15 + 50 * i, 2), random_str, text_color, font)
    # 记录给哪个请求发了什么验证码
    request.session['code'] = code_str

    # 使用画笔将文字画到画布上
    # draw.text((10, 20), "X", text_color, font)
    # draw.text((40, 20), "Q", text_color, font)
    # draw.text((60, 20), "W", text_color, font)

    # 获得一个缓存区
    buf = io.BytesIO()
    # 将图片保存到缓存区
    image.save(buf, 'png')
    # 将缓存区的内容返回给前端 .getvalue 是把缓存区的所有数据读取
    return HttpResponse(buf.getvalue(), 'image/png')


# 显示后台主页
def to_admin_index(request):
    # user = User.objects.get(user_name='zyk')
    # print(user.__dict__)
    return render(request, 'admin-index.html')


# 显示欢迎页面
def to_welcome(request):
    return render(request, 'welcome.html')


# 显示轮播列表页面
def to_slide(request):
    return render(request, 'slide/slide-list.html')


# 显示添加轮播页面
def add_slide_dis(request):
    return render(request, 'slide/add-slide.html')


# 显示修改轮播欢迎页面
def edit_slide_dis(request, id):
    slide = Slide.objects.get(id=id)
    return render(request, 'slide/edit-slide.html', {'slide': slide})


# 轮播API
class SlideView(APIView):
    # 获取轮播列表
    def get(self, request):
        key = request.GET['key']
        slide_list = Slide.objects.filter(title__contains=key)
        slide_list = slide_list.order_by('-gmt_created')
        page = StandardPagination()
        page_data = page.paginate_queryset(queryset=slide_list, request=request, view=self)
        slides_ser = SlideSerializers(instance=page_data, many=True)
        return get_page_response(page, slides_ser.data)

    # 创建轮播
    def post(self, request):
        slide = SlideSerializers(data=request.data)  # 反序列化成model
        if slide.is_valid():  # 验证数据
            slide.save()  # 保存轮播
            json_data = {"msg": "添加成功", "code": 1}
        else:
            json_data = {"msg": slide.error_messages, "code": 0}
        return Response(json_data)

    # 更新轮播
    def patch(self, request):
        slide = SlideSerializers(Slide(), data=request.data, partial=True)
        if slide.is_valid():
            slide.save()
            json_data = {"msg": "修改成功", "code": 1}
        else:
            json_data = {"msg": slide.error_messages, "code": 0}
        return Response(json_data)

    # 删除轮播
    def delete(self, request):
        delete = QueryDict(request.body)
        id = delete.get('id')
        try:
            slide = Slide.objects.get(id=id)
            slide.delete()
            json_data = {"msg": "删除成功", "code": 1}
        except Exception as e:
            json_data = {"msg": "删除失败", "code": 0}
            print(e)
        return Response(json_data)


# 登录模块
class LoginView(APIView):
    # 执行post请求:验证登录
    def post(self, request, format=None):
        user_name = request.POST['user_name']
        pwd = request.POST['pwd']
        code = request.POST['code']
        correct_code = request.session['code']
        # 校验验证码
        if code.lower() == correct_code.lower():
            try:
                user_id = request.session['user_id']
                json_data = {"msg": "已登录,请勿重复登录", "code": 0}
            except KeyError:
                try:
                    user = User.objects.get(Q(user_name=user_name) | Q(email=user_name))
                    if not check_password(pwd, user.password):  # 密码错误
                        json_data = {"msg": "密码错误", "code": 0}
                    else:
                        if user.login_power == 1:  # 已授权
                            request.session['user_name'] = user.user_name  # 密码正确且有登录权限（将用户信息存入session）
                            request.session['user_id'] = user.id
                            request.session['user_authority'] = user.user_authority
                            if user.user_authority == 1:  # 超管
                                json_data = {"msg": "超管登录成功，正在跳转......", "code": 2}
                            else:  # 普通用户
                                json_data = {"msg": "登录成功，正在跳转......", "code": 1}
                        else:  # 未授权
                            json_data = {"msg": "未授权", "code": 0}
                except User.DoesNotExist:  # 用户不存在
                    json_data = {"msg": "不存在该用户", "code": 0}
        else:
            json_data = {"msg": "验证码错误", "code": 0}
        return Response(json_data)

    # 注销
    def delete(self, request):
        try:
            del request.session['user_name']
            del request.session['user_id']
            del request.session['user_authority']
        except KeyError:
            pass
        return Response({"code": 1})


# 注册模块
class RegisterView(APIView):

    def post(self, request, format=None):
        user_name = request.POST['user_name']
        password = request.POST['pwd']
        email = request.POST['email']
        email_code = request.POST['email_code']
        user_data = {"user_name": user_name, "password": make_password(password), "email": email}
        user = UserSerializers(data=user_data)  # 反序列化成model类
        old_user = User.objects.filter(Q(user_name=request.POST['user_name']) | Q(email=email)).first()
        if old_user:  # 已经存在该用户
            json_data = {"msg": "已注册", "code": 0}
        else:  # 可以注册
            email_code_check = request.session.get('email_code', None)
            if email_code_check is None or email_code != email_code_check:
                json_data = {"msg": "验证码无效或错误", "code": 0}
            else:
                try:
                    user.is_valid()
                    user.save()  # 保存数据
                    json_data = {"msg": "注册成功", "code": 1}
                except Exception as e:
                    json_data = {"msg": "注册失败", "code": 0}
                    print(e)
        return Response(json_data)


# 显示用户列表页面
def user_dis(request):
    return render(request, 'user/user_list.html')


# 显示修改密码页面
def edit_pwd_dis(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, 'user/edit_pwd.html', {'user': user})


# 用户管理模块
class UserView(APIView):
    # 获取用户列表（分页 + 搜索）
    def get(self, request, format=True):
        key = request.GET.get('key', '')
        user_list = User.objects.filter(Q(user_authority=0),
                                        Q(user_name__contains=key) | Q(mobile_phone__contains=key) | Q(
                                            email__contains=key)).order_by('id')
        # print(user_list.values())
        page = StandardPagination()
        page_users = page.paginate_queryset(queryset=user_list, request=request, view=self)
        users_ser = UserSerializers(instance=page_users, many=True)
        return get_page_response(page, users_ser.data)

    # 修改用户密码
    def post(self, request, format=None):
        user_id = request.POST['id']
        password = request.POST['password']
        user = User.objects.get(id=user_id)
        if check_password(password, user.password):
            json_data = {"msg": "不能与原密码相同", "code": 0}
        else:
            user.password = make_password(password)
            try:
                user.save()
                json_data = {"msg": "修改成功", "code": 1}
            except Exception as e:
                json_data = {"msg": "修改失败", "code": 0}
                print(e)
        return Response(json_data)

    # 用户授权/禁用
    def put(self, request, format=None):
        # 手动处理request.body中的参数
        put = QueryDict(request.body)
        user_id = put.get('id')
        try:
            user = User.objects.get(id=user_id)
            if user.login_power == 1:  # 判断用户原来的权限
                user.login_power = 0
                json_data = {"msg": "已停用", "code": 1}
            else:
                user.login_power = 1
                json_data = {"msg": "已启用", "code": 2}
            user.save()
        except Exception as e:
            json_data = {"msg": "操作失败", "code": 2}
            print(e)
        return Response(json_data)

    # 删除用户
    def delete(self, request, format=None):
        # 手动处理request.body中的参数
        delete = QueryDict(request.body)
        user_id = delete.get('id')
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            json_data = {"msg": "删除成功", "code": 1}
        except Exception as e:
            json_data = {"msg": "删除失败", "code": 0}
            print(e)
        return Response(json_data)


# 显示分类列表页
def sort_dis(request):
    return render(request, 'sort/sort_list.html')


# 显示添加分类页面
def sort_add_dis(request):
    return render(request, 'sort/add_sort.html')


# 显示修改分类页面
def sort_eidt_dis(request, id):
    category = Category.objects.get(id=id)
    parent_sorts = Category.objects.filter(is_parent=1)
    return render(request, 'sort/edit_sort.html', {"category": category, "parent_sorts": parent_sorts})


# 获取所有主类列表
@api_view(['GET'])
def get_parent_sorts(request):
    parent_sorts = Category.objects.filter(is_parent=1)
    parent_sorts_ser = CategorySerializers(instance=parent_sorts, many=True)
    return JsonResponse(parent_sorts_ser.data, safe=False)


# 根据parent_id获取所有次级分类列表
@api_view(['GET'])
def get_child_sorts(request):
    parent_id = request.GET['parent_id']
    parent = Category.objects.get(id=parent_id)
    child_sorts = Category.objects.filter(parent=parent)
    child_sorts_ser = CategorySerializers(instance=child_sorts, many=True)
    return Response(child_sorts_ser.data)


# 标签页显示
def label_dis(request):
    return render(request, 'label/label-list.html')


# 添加标签页显示
def label_add_dis(request):
    return render(request, 'label/add-label.html')


# 修改标签页显示
def label_edit_dis(request, id):
    category = Category.objects.get(id=id)
    parent_sorts = Category.objects.filter(is_parent=1)
    return render(request, 'label/edit-label.html', {"category": category, "parent_sorts": parent_sorts})


# 文章分类模块
class SortView(APIView):

    def get(self, request, format=None):  # 获取分类列表（分页 + 搜索）
        global category_list
        key = request.GET['key']
        is_parent = request.GET['is_parent']
        parent_id = request.GET.get('parent_id')
        if is_parent == '0':
            if parent_id == '' or parent_id is None:
                category_list = Category.objects.filter(category_name__contains=key, is_parent=0)
            else:
                category_list = Category.objects.filter(category_name__contains=key, parent_id=int(parent_id))
        elif is_parent == '1':
            category_list = Category.objects.filter(category_name__contains=key, is_parent=1)
        elif is_parent == '' or is_parent is None:
            category_list = Category.objects.filter(category_name__contains=key)
        category_list = category_list.order_by('-gmt_created')
        page = StandardPagination()
        page_sorts = page.paginate_queryset(queryset=category_list, request=request, view=self)
        sorts_ser = CategorySerializers(instance=page_sorts, many=True)
        return get_page_response(page, sorts_ser.data)

    def post(self, request, format=None):  # 创建分类
        # 反序列化，将json转化成model
        category = CategorySerializers(data=request.data)
        if category.is_valid():
            # 验证分类名重复性
            if Category.objects.filter(category_name=category.validated_data['category_name']).first() is None:
                category.save()
                json_data = {"msg": "添加成功", "code": 1}
            else:
                json_data = {"msg": "已存在该分类", "code": 0}
        else:
            # print(category.errors)
            json_data = {"msg": "添加失败", "code": 0}
        return Response(json_data)

    def patch(self, request, format=None):  # 更新分类
        category = CategorySerializers(Category, data=request.data, partial=True)
        if category.is_valid():
            # print(category.validated_data)
            category.save()
            json_data = {"msg": "修改成功", "code": 1}
        else:
            json_data = {"msg": "修改失败", "code": 0}
        return Response(json_data)

    def delete(self, request, format=None):  # 删除分类
        delete = QueryDict(request.body)
        id = delete.get('id')
        try:
            category = Category.objects.get(id=id)
            category.delete()
            json_data = {"msg": "删除成功", "code": 1}
        except Exception as e:
            json_data = {"msg": "删除失败", "code": 0}
            print(e)
        return Response(json_data)


# 文章列表页显示
def article_dis(request):
    return render(request, 'article/article_list.html')


# 添加文章页面显示
def add_article_dis(request):
    return render(request, 'article/add_article.html')


# 编辑文章页面显示
def edit_article_dis(request, id):
    article = Article.objects.get(id=id)
    category = Category.objects.get(id=article.category_id)
    parent_sorts = Category.objects.filter(is_parent=1)
    child_sorts = Category.objects.filter(is_parent=0)
    # form = CreateArticleForm(instance=article)
    return render(request, 'article/edit_article.html',
                  {"article": article, "category": category, "parent_sorts": parent_sorts,
                   "child_sorts": child_sorts})


# 文章管理模块
class ArticleView(APIView):
    # 获取文章列表(分页 + 搜索)
    def get(self, request):
        global article_list
        parent_id = request.GET['parent_id']
        child_id = request.GET['child_id']
        key = request.GET['key']
        try:
            if parent_id == '' and child_id == '':
                article_list = Article.objects.filter(
                    Q(title__contains=key) | Q(user__user_name__contains=key))
            elif parent_id != '' and child_id == '':
                article_list = Article.objects.filter(Q(category__parent_id=parent_id),
                                                      Q(title__contains=key) | Q(
                                                          user__user_name__contains=key))
            elif parent_id != '' and child_id != '':
                article_list = Article.objects.filter(Q(category__id=child_id), Q(category__parent_id=parent_id),
                                                      Q(title__contains=key) | Q(
                                                          user__user_name__contains=key))
        except KeyError:
            article_list = Article.objects.filter(Q(title__contains=key) | Q(user__user_name__contains=key))
        article_list = article_list.order_by('-gmt_created')
        page = FrontPagination()
        page_articles = page.paginate_queryset(queryset=article_list, request=request, view=self)
        articles_ser = ArticleSerializers(instance=page_articles, many=True)
        return get_page_response(page, articles_ser.data)

    # 创建文章
    def post(self, request):
        article = ArticleSerializers(data=request.data)
        if article.is_valid():
            article.save()
            json_data = {"msg": "添加成功", "code": 1}
        else:
            print(article.error_messages)
            json_data = {"msg": article.errors, "code": 0}
        return Response(json_data)

    # 修改文章
    def patch(self, request):
        article = ArticleSerializers(Article(), data=request.data)
        if article.is_valid():
            article.save()
            json_data = {"msg": "修改成功", "code": 1}
        else:
            json_data = {"msg": article.errors, "code": 0}
        return Response(json_data)

    # 删除文章
    def delete(self, request):
        delete = QueryDict(request.body)
        id = delete.get('id')
        try:
            article = Article.objects.get(id=id)
            article.delete()
            json_data = {"msg": "删除成功", "code": 1}
        except Exception as e:
            json_data = {"msg": "删除失败", "code": 0}
            print(e)
        return Response(json_data)


# 显示评论列表页面
def to_comment_list(request):
    return render(request, 'comment/comment-list.html')


# 评论API
class CommentView(APIView):
    # 获取评论数据(分页 + 搜索)
    def get(self, request):
        global comment_list
        type = request.GET.get('type')
        date_min = request.GET.get('date_min')
        date_max = request.GET.get('date_max')
        key = request.GET.get('key')
        if date_min != '':
            # str转datetime
            date_min = datetime.datetime.strptime(date_min, '%Y-%m-%d')
        if date_max != '':
            date_max = datetime.datetime.strptime(date_max, '%Y-%m-%d') + datetime.timedelta(hours=24)
        if type == '' and date_min == '' and date_max == '':
            comment_list = Comment.objects.filter(Q(user__user_name__contains=key) | Q(content__contains=key))
        elif type != '' and date_min == '' and date_max == '':
            if type == '1':
                comment_list = Comment.objects.filter(Q(user__user_name__contains=key) | Q(content__contains=key),
                                                      Q(to_comment_id__isnull=True))
            if type == '2':
                comment_list = Comment.objects.filter(Q(user__user_name__contains=key) | Q(content__contains=key),
                                                      Q(to_comment_id__isnull=False))
        elif type == '' and date_min != '' and date_max != '':
            comment_list = Comment.objects.filter(Q(user__user_name__contains=key) | Q(content__contains=key),
                                                  Q(gmt_created__gte=date_min) & Q(gmt_created__lte=date_max))
        elif type == '' and date_min != '' and date_max == '':
            comment_list = Comment.objects.filter(Q(user__user_name__contains=key) | Q(content__contains=key),
                                                  Q(gmt_created__gte=date_min))
        elif type == '' and date_min == '' and date_max != '':
            comment_list = Comment.objects.filter(Q(user__user_name__contains=key) | Q(content__contains=key),
                                                  Q(gmt_created__lte=date_max))
        elif type != '' and date_min != '' and date_max != '':
            if type == '1':
                comment_list = Comment.objects.filter(Q(user__user_name__contains=key) | Q(content__contains=key),
                                                      Q(to_comment_id__isnull=True),
                                                      Q(gmt_created__gte=date_min) & Q(gmt_created__lte=date_max))
            if type == '2':
                comment_list = Comment.objects.filter(Q(user__user_name__contains=key) | Q(content__contains=key),
                                                      Q(to_comment_id__isnull=False),
                                                      Q(gmt_created__gte=date_min) & Q(gmt_created__lte=date_max))
        elif type != '' and date_min != '' and date_max == '':
            if type == '1':
                comment_list = Comment.objects.filter(Q(user__user_name__contains=key) | Q(content__contains=key),
                                                      Q(to_comment_id__isnull=True),
                                                      Q(gmt_created__gte=date_min))
            if type == '2':
                comment_list = Comment.objects.filter(Q(user__user_name__contains=key) | Q(content__contains=key),
                                                      Q(to_comment_id__isnull=False),
                                                      Q(gmt_created__gte=date_min))
        elif type != '' and date_min == '' and date_max != '':
            if type == '1':
                comment_list = Comment.objects.filter(Q(user__user_name__contains=key) | Q(content__contains=key),
                                                      Q(to_comment_id__isnull=True),
                                                      Q(gmt_created__lte=date_max))
            if type == '2':
                comment_list = Comment.objects.filter(Q(user__user_name__contains=key) | Q(content__contains=key),
                                                      Q(to_comment_id__isnull=False),
                                                      Q(gmt_created__lte=date_max))
        comment_list = comment_list.order_by('-gmt_created')
        page = FrontPagination()
        page_data = page.paginate_queryset(queryset=comment_list, request=request, view=self)
        comment_ser = CommentSerializers(instance=page_data, many=True)
        return get_page_response(page, comment_ser.data)

    # 删除评论
    def delete(self, request):
        delete = QueryDict(request.body)
        id = delete.get('id')
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


# 显示友情链接列表
def links_dis(request):
    return render(request, 'link/link-list.html')


# 显示添加友情链接页面
def link_add_dis(request):
    return render(request, 'link/add-link.html')


# 显示修改友情链接页面
def link_edit_dis(request, id):
    link = Link.objects.get(id=id)
    return render(request, 'link/edit-link.html', {"link": link})


# 批量删除友情链接
@api_view(['POST'])
def delete_checked_links(request):
    ids = request.POST.get('ids')
    try:
        Link.objects.extra(where=['id IN (' + ids + ')']).delete()
        json_data = {"msg": "删除成功", "code": 1}
    except:
        json_data = {"msg": "删除失败", "code": 0}
    return Response(json_data)


# 友链API
class LinkView(APIView):
    # 获取友链列表(分页 + 搜索)
    def get(self, request):
        key = request.GET.get('key')
        link_list = Link.objects.filter(link_name__icontains=key).order_by('-created_time')
        page = StandardPagination()
        page_data = page.paginate_queryset(queryset=link_list, request=request, view=self)
        links_ser = LinkSerializers(instance=page_data, many=True)
        return get_page_response(page, links_ser.data)

    # 创建友链
    def put(self, request):
        link = LinkSerializers(data=request.data)
        if link.is_valid():
            link.save()
            json_data = {"msg": "添加成功", "code": 1}
        else:
            json_data = {"msg": "添加失败", "code": 0}
        return Response(json_data)

    # 修改友链
    def patch(self, request):
        link = LinkSerializers(Link(), data=request.data)
        if link.is_valid():
            link.save()
            json_data = {"msg": "修改成功", "code": 1}
        else:
            json_data = {"msg": "修改失败", "code": 0}
        return Response(json_data)

    # 删除友链
    def delete(self, request):
        delete = QueryDict(request.body)
        id = delete.get('id')
        try:
            link = Link.objects.get(id=id)
            link.delete()
            json_data = {"msg": "删除成功", "code": 1}
        except Exception as e:
            json_data = {"msg": "删除失败", "code": 0}
            print(e)
        return Response(json_data)


def site_setting_dis(request):
    site = Site.objects.all().first()
    return render(request, 'site/site-setting.html', {'site': site})


# 站点API
class SiteView(APIView):
    def post(self, request):
        site = SiteSerializers(data=request.data)
        if site.is_valid():
            site.save()
            json_data = {"msg": "添加成功", "code": 1}
        else:
            json_data = {"msg": "添加失败", "code": 0}
        return Response(json_data)

    def patch(self, request):
        site = SiteSerializers(Site(), data=request.data)
        if site.is_valid():
            site.save()
            json_data = {"msg": "修改成功", "code": 1}
        else:
            json_data = {"msg": "修改失败", "code": 0}
        return Response(json_data)
