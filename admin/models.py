import uuid

from django.db import models
from django.urls import reverse


def article_image_upload_to(instance, filename):
    return 'article/{uuid}/{filename}'.format(uuid=uuid.uuid4().hex, filename=filename)


def image_upload_to(instance, filename):
    return 'slide/{uuid}/{filename}'.format(uuid=uuid.uuid4().hex, filename=filename)


def user_img_upload_to(instance, filename):
    return 'user_img/{uuid}/{filename}'.format(uuid=uuid.uuid4().hex, filename=filename)


class Article(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, default=None)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, default=None)
    is_like = models.IntegerField(blank=True, null=True, default=0)
    is_show = models.IntegerField(blank=True, null=True, default=1)
    title = models.CharField(max_length=64)
    # img = models.ImageField(upload_to=article_image_upload_to, max_length=100)
    img = models.TextField(max_length=100, default=None)
    content = models.TextField()
    comment_number = models.IntegerField(default=0, blank=True, null=True)
    read_number = models.IntegerField(default=0, blank=True, null=True)
    gmt_created = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    gmt_modified = models.DateTimeField(blank=True, null=True, auto_now=True)
    remark = models.CharField(max_length=255, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('articleDetail', kwargs={'article_id': self.id})

    class Meta:
        db_table = "mb_article"


class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE)
    is_parent = models.IntegerField()
    category_name = models.CharField(max_length=32)
    gmt_created = models.DateTimeField(blank=True, null=True, auto_now_add=True)  # auto_now_add为添加时的时间，更新对象时不会有变动。
    gmt_modified = models.DateTimeField(blank=True, null=True, auto_now=True)  # auto_now无论是你添加还是修改对象，时间为你添加或者修改的时间。
    remark = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "mb_category"


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    # user_img = models.ImageField(upload_to=user_img_upload_to, max_length=100, blank=True, null=True)
    user_img = models.CharField(max_length=100, blank=True, null=True)
    user_name = models.CharField(max_length=32)
    password = models.CharField(max_length=86)
    login_power = models.IntegerField()
    login_state = models.IntegerField()
    user_authority = models.IntegerField()
    mobile_phone = models.CharField(max_length=32, blank=True, null=True)
    email = models.CharField(max_length=32, blank=True, null=True)
    nick_name = models.CharField(max_length=32, blank=True, null=True)
    sex = models.IntegerField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    login_time = models.DateTimeField(blank=True, null=True)
    register_time = models.DateTimeField(blank=True, null=True)
    last_login_time = models.DateTimeField(blank=True, null=True)
    login_count = models.IntegerField(blank=True, null=True)
    person_intro = models.TextField(blank=True, null=True)
    gmt_created = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    gmt_modified = models.DateTimeField(blank=True, null=True, auto_now=True)
    remark = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "mb_user"


class Slide(models.Model):
    id = models.BigAutoField(primary_key=True)
    img = models.ImageField(upload_to=image_upload_to, max_length=100, blank=True, null=True)
    title = models.CharField(max_length=100)
    gmt_created = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    gmt_modified = models.DateTimeField(blank=True, null=True, auto_now=True)
    remark = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "mb_slide"


class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    to_comment = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user', default=None)
    reply_user = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True, related_name='reply_user')
    article = models.ForeignKey('Article', on_delete=models.CASCADE, default=None)
    content = models.CharField(max_length=255, blank=True, null=True)
    # content = RichTextUploadingField(max_length=255)
    liked_number = models.IntegerField(blank=True, null=True, default=0)
    reply_count = models.IntegerField(blank=True, null=True, default=0)
    gmt_created = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    gmt_modified = models.DateTimeField(blank=True, null=True, auto_now=True)
    remark = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "mb_comment"


class Like(models.Model):
    id = models.BigAutoField(primary_key=True)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, default=None)
    user = models.ForeignKey('User', on_delete=models.CASCADE, default=None)
    article = models.ForeignKey('Article', on_delete=models.CASCADE, default=None)
    is_like = models.IntegerField(blank=True, null=True)
    gmt_created = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    gmt_modified = models.DateTimeField(blank=True, null=True, auto_now=True)
    remark = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "mb_like"


class Link(models.Model):
    id = models.BigAutoField(primary_key=True)
    link_name = models.CharField(max_length=255)
    link_url = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    created_time = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    modified_time = models.DateTimeField(blank=True, null=True, auto_now=True)
    remark = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "mb_link"


class Site(models.Model):
    site_name = models.CharField(max_length=255)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    logo = models.CharField(max_length=100, null=True, blank=True)
    copyright_info = models.CharField(max_length=255, null=True, blank=True)
    record_number = models.CharField(max_length=255, null=True, blank=True)
    statistic_code = models.TextField(max_length=1000, null=True, blank=True)
    gmt_created = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    gmt_modified = models.DateTimeField(blank=True, null=True, auto_now=True)
    remark = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "mb_site"

