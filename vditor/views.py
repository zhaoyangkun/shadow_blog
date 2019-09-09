import os
import uuid

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from PIL import Image


# 上传文件（默认保存本地）
@require_http_methods(['POST'])
def img_upload(request):
    img_files = request.FILES.getlist('files')  # 获取多文件对象
    images = []
    try:
        root_path = settings.MEDIA_ROOT + settings.VDITOR_UPLOAD  # 获取文件上传目录
        url_path = settings.MEDIA_URL + settings.VDITOR_UPLOAD  # 获取虚拟地址
    except AttributeError:  # 用户未配置，采用默认配置
        root_path = settings.MEDIA_ROOT + '/vditor/'
        url_path = settings.MEDIA_URL + '/vditor/'
    try:
        for file in img_files:  # 遍历文件
            if not os.path.exists(root_path):  # 判断文件上传目录是否存在
                os.makedirs(root_path)  # 不存在，则创建
            file_name = create_file_name(file)  # 获取文件名
            file_path = '{}/{}'.format(root_path, file_name)  # 拼接文件保存路径
            with open(file_path, 'wb') as f:  # 保存图片
                for c in file.chunks():
                    f.write(c)
            compress_img(file_path, 0.8)  # 压缩图片，默认压缩比0.8
            images.append('{}{}'.format(os.path.join(url_path.replace('//', '/')), file_name))
        json_data = {"msg": "上传成功", "code": 1, "images": images}  # 构建，保存URL路径
    except Exception as e:
        print(e)
        json_data = {"msg": "上传失败", "code": 0}
    return JsonResponse(json_data, safe=False)


# 利用UUID生成文件名，防止重名
def create_file_name(file):
    type_name = file.name[file.name.index('.'):]  # 获取文件后缀
    file_name = '{}{}'.format(uuid.uuid4(), type_name)  # 生成文件名
    return file_name


# 压缩图片
def compress_img(file_path, rate):
    image = Image.open(file_path)  # 获得图像
    width = int(image.width * rate)  # 宽
    height = int(image.height * rate)  # 高
    image.thumbnail((width, height), Image.ANTIALIAS)  # 生成缩略图
    image.save(file_path)
