import os
import urllib.request
import uuid

from django.test import TestCase

# Create your tests here.
# 将图片保存至本地
from my_blog import settings


class TestDefault(TestCase):

    def upload_user_img_1(self):
        img_url = 'https://avatars3.githubusercontent.com/u/29301950?v=4'
        folder_path = os.path.join(settings.BASE_DIR, 'media', 'user_img')  # 图片保存文件夹路径
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)  # 不存在，则创建
        try:
            img_name = '{}{}'.format(uuid.uuid4().hex, '.jpg')  # 生成文件名
            file_path = os.path.join(folder_path, img_name)
            urllib.request.urlretrieve(img_url, filename=file_path)
            # return os.path.join('user_img', img_name)
        except Exception as e:
            print(e)
            # return None
