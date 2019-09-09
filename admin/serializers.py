import os
import uuid

from django.conf import settings
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from admin.models import User, Category, Article, Slide, Comment, Link, Site
from vditor.views import compress_img


class UserSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    user_img = serializers.ImageField(required=False, max_length=100, error_messages={"max_length": "名称长度不能超过100"})
    user_name = serializers.CharField(max_length=32, required=True)
    password = serializers.CharField(max_length=86, required=False, write_only=True)
    login_power = serializers.IntegerField(default=1, required=False)
    login_state = serializers.IntegerField(default=0, required=False)
    user_authority = serializers.IntegerField(required=False)
    mobile_phone = serializers.CharField(max_length=32, required=False)
    email = serializers.CharField(max_length=32, required=False)
    nick_name = serializers.CharField(max_length=32, required=False)
    sex = serializers.IntegerField(default=1, required=False)
    birthday = serializers.DateField(required=False)
    login_time = serializers.DateTimeField(required=False)
    register_time = serializers.DateTimeField(required=False)
    last_login_time = serializers.DateTimeField(required=False)
    login_count = serializers.IntegerField(required=False)
    person_intro = serializers.CharField(required=False)
    gmt_created = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')
    gmt_modified = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')
    remark = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = User
        # field = ("id", "user_name", "password", "nick_name", "gmt_created", "gmt_modified", "remark")
        fields = '__all__'  # 这个是将所有的字段都序列化

    def create(self, validated_data):
        user_authority = 0
        if User.objects.count() == 0:
            user_authority = 1
        return User.objects.create(user_authority=user_authority, **validated_data)  # 调用Idc模型进行create操作

    def update(self, instance, validated_data):
        user = User.objects.get(user_name=validated_data['user_name'])
        file = validated_data.get('user_img', '')
        # 图片不为空，保存图片
        if file != '':
            try:
                img_name = '{}{}'.format(uuid.uuid4().hex, '.jpg')  # 生成文件名
                folder_path = os.path.join(settings.BASE_DIR, 'media', 'user_img')
                if not os.path.exists(folder_path):
                    os.mkdir(folder_path)
                file_path = os.path.join(folder_path, img_name)  # 图片路径
                with open(file_path, 'wb') as f:
                    for c in file.chunks():
                        f.write(c)
                user.user_img = 'user_img/' + img_name
            except IOError as e:
                print(e)
        user.nick_name = validated_data.get('nick_name', user.nick_name)
        user.sex = validated_data.get('sex', user.sex)
        if validated_data.get('password'):
            user.password = make_password(validated_data.get('password'))
        user.birthday = validated_data.get('birthday', user.birthday)
        user.mobile_phone = validated_data.get('mobile_phone', user.mobile_phone)
        user.save()
        return user


class ParentCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'  # 这个是将所有的字段都序列化


class CategorySerializers(serializers.ModelSerializer):
    # parent = serializers.CharField(source='parent.category_name', required=False)
    # parent_id = serializers.CharField(source='parent.id', required=False)
    id = serializers.IntegerField(required=False)
    parent = ParentCategorySerializers(required=False)
    parent_id = serializers.CharField(source='parent.id', required=False)

    class Meta:
        model = Category
        fields = '__all__'

    def create(self, validated_data):
        try:
            parent_data = validated_data.pop('parent')
            parent = Category.objects.get(id=parent_data['id'])
            category = Category.objects.create(parent=parent, **validated_data)
        except KeyError:
            category = Category.objects.create(**validated_data)
        return category

    def update(self, instance, validated_data):
        try:
            parent_data = validated_data.pop('parent')
            parent = Category.objects.get(id=parent_data['id'])
            category = Category.objects.filter(id=validated_data.pop('id')).update(parent=parent, **validated_data)
        except KeyError:
            category = Category.objects.filter(id=validated_data.pop('id')).update(**validated_data)
        return category


class ArticleSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    user = UserSerializers(required=False)
    user_id = serializers.CharField(source='user.id', required=False)
    category = CategorySerializers(required=False)
    category_id = serializers.CharField(source='category.id', required=False)
    parent_id = serializers.CharField(source='category.parent.id', required=False)
    img = serializers.ImageField(required=False, max_length=100, error_messages={"max_length": "名称长度不能超过100"})
    content = serializers.CharField(required=True, max_length=100000,
                                    error_messages={"max_length": "不能超过100000字", "blank": "请输入文章内容",
                                                    "required": "请输入文章内容"})
    gmt_created = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')
    gmt_modified = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Article
        fields = "__all__"

    # 重写创建对象方法
    def create(self, validated_data):
        file = validated_data.pop('img')
        img_url = ""
        try:
            img_name = '{}{}'.format(uuid.uuid4().hex, '.jpg')  # 生成文件名
            folder_path = os.path.join(settings.BASE_DIR, 'media', 'article')
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)
            file_path = os.path.join(folder_path, img_name)  # 图片路径
            with open(file_path, 'wb') as f:
                for c in file.chunks():
                    f.write(c)
            compress_img(file_path, 0.6)  # 压缩图片
            img_url = 'article/' + img_name
        except IOError as e:
            print(e)
        category_data = validated_data.pop('category')
        user_data = validated_data.pop('user')
        category = Category.objects.get(id=category_data['id'])
        user = User.objects.get(id=user_data['id'])
        return Article.objects.create(category=category, user=user, img=img_url, **validated_data)

    # 重写更新对象方法
    def update(self, instance, validated_data):
        category_data = validated_data.pop('category')
        user_data = validated_data.pop('user')
        category = Category.objects.get(id=category_data['id'])
        user = User.objects.get(id=user_data['id'])
        article = Article.objects.get(id=validated_data['id'])
        article.category = category
        article.user = user
        article.title = validated_data['title']
        article.content = validated_data['content']
        article.is_like = validated_data['is_like']
        article.is_show = validated_data['is_show']
        try:
            file = validated_data.pop('img')
            try:
                img_name = '{}{}'.format(uuid.uuid4().hex, '.jpg')  # 生成文件名
                folder_path = os.path.join(settings.BASE_DIR, 'media', 'article')
                if not os.path.exists(folder_path):
                    os.mkdir(folder_path)
                file_path = os.path.join(folder_path, img_name)  # 图片路径
                with open(file_path, 'wb') as f:
                    for c in file.chunks():
                        f.write(c)
                compress_img(file_path, 0.6)  # 压缩图片
                img_url = 'article/' + img_name
                article.img = img_url
            except IOError as e:
                print(e)
        except KeyError:
            print("******无图片")
            pass
        article.save()
        return article


class SlideSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    img = serializers.ImageField(required=False, max_length=100, error_messages={"max_length": "名称长度不能超过100"})

    class Meta:
        model = Slide
        fields = "__all__"

    def update(self, instance, validated_data):
        print(validated_data)
        slide = Slide.objects.get(id=validated_data['id'])
        try:
            img = validated_data['img']
            slide.img = img
        except KeyError:
            pass
        slide.title = validated_data['title']
        slide.remark = validated_data['remark']
        slide.save()
        return slide


class SelfCommentSerializers(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(many=True, required=True)
    class Meta:
        model = Comment
        fields = "__all__"


class CommentSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    user = UserSerializers(required=False)
    user_id = serializers.CharField(source='user.id', required=False)
    reply_user = UserSerializers(required=False)
    reply_user_id = serializers.CharField(source='reply_user.id', required=False)
    to_comment = SelfCommentSerializers(required=False)
    to_comment_id = serializers.CharField(source='to_comment.id', required=False)
    article = ArticleSerializers(required=False)
    article_id = serializers.CharField(source='article.id', required=False)
    gmt_created = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')
    gmt_modified = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Comment
        fields = "__all__"

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        article_data = validated_data.pop('article')
        user = User.objects.get(id=user_data['id'])
        article = Article.objects.get(id=article_data['id'])
        try:
            reply_user_data = validated_data.pop('reply_user')
            to_comment_data = validated_data.pop('to_comment')
            article.comment_number = article.comment_number + 1
            article.save()
            return Comment.objects.create(user=user, article=article, reply_user_id=reply_user_data['id'],
                                          to_comment_id=to_comment_data['id'],
                                          **validated_data)
        except KeyError:
            article.comment_number = article.comment_number + 1
            article.save()
            return Comment.objects.create(user=user, article=article, **validated_data)


class LinkSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Link
        fields = "__all__"

    def update(self, instance, validated_data):
        link = Link.objects.get(id=validated_data['id'])
        link.link_name = validated_data['link_name']
        link.link_url = validated_data['link_url']
        link.description = validated_data['description']
        link.save()
        return link


class SiteSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    logo = serializers.ImageField(required=False, max_length=100)

    class Meta:
        model = Site
        fields = "__all__"

    def create(self, validated_data):
        file = validated_data.pop("logo", "")
        logo = ""
        if file != "":
            logo = upload_img('logo', validated_data, 'site', 0.8)
        return Site.objects.create(logo=logo, **validated_data)

    def update(self, instance, validated_data):
        site = Site.objects.get(id=validated_data.get('id'))
        file = validated_data.get("logo", "")
        if file != "":
            logo = upload_img('logo', validated_data, 'site', 0.8)
            site.logo = logo
        site.site_name = validated_data.get('site_name', site.site_name)
        site.keywords = validated_data.get('keywords', site.keywords)
        site.description = validated_data.get('description', site.description)
        site.author = validated_data.get('author', site.author)
        site.copyright_info = validated_data.get('copyright_info', site.copyright_info)
        site.record_number = validated_data.get('record_number', site.record_number)
        site.statistic_code = validated_data.get('statistic_code', site.statistic_code)
        site.save()
        return site


# 上传图片
def upload_img(pop_str, validated_data, related_path, rate):
    '''
    :param pop_str: 键值
    :param validated_data: 数据
    :param related_path: 保存相对路径
    :param rate: 压缩率
    :return: 图片URL访问地址
    '''
    img_url = ''
    file = validated_data.pop(pop_str)
    try:
        img_name = '{}{}'.format(uuid.uuid4().hex, '.jpg')  # 生成文件名
        folder_path = os.path.join(settings.BASE_DIR, 'media', related_path)
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        file_path = os.path.join(folder_path, img_name)  # 图片路径
        with open(file_path, 'wb') as f:
            for c in file.chunks():
                f.write(c)
        compress_img(file_path, rate)  # 压缩图片
        img_url = "{path}/{name}".format(path=related_path, name=img_name)
    except IOError as e:
        print(e)
    return img_url
