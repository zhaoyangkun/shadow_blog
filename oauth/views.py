import os
import time
import urllib.request
import uuid

from django.contrib.auth.hashers import make_password
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from admin.models import User
from django.conf import settings
from oauth.models import OAuth
from oauth.oauth import OAuthGithub


def github_login(request):
    try:
        oauth_git = OAuthGithub(settings.GITHUB_CLIENT_ID, settings.GITHUB_CLIENT_SECRET, settings.GITHUB_CALLBACK_URL)
        url = oauth_git.get_auth_url()
        json_data = {'msg': '正在跳转至授权页面...', 'code': 1, 'data': url}
    except AttributeError:
        json_data = {'msg': '未配置授权信息', 'code': 0}
    return JsonResponse(json_data, safe=False)


def github_check(request):
    type = '1'
    request_code = request.GET.get("code")
    oauth_git = OAuthGithub(settings.GITHUB_CLIENT_ID, settings.GITHUB_CLIENT_SECRET, settings.GITHUB_CALLBACK_URL)
    try:
        oauth_git.get_access_token(request_code)  # 获取access token
        time.sleep(0.1)  # 此处需要休息一下，避免发送urlopen的10060错误
    except Exception as e:  # 获取token失败，反馈失败信息
        print(e)
        return render(request, 'login.html', {"error": "获取token失败"})
    infos = oauth_git.get_user_info()  # 获取用户信息
    print("用户信息: " + str(infos))
    open_id = infos.get('id', '')
    nickname = infos.get('login', '')
    image_url = infos.get('avatar_url', '')
    email = infos.get('email', '')
    oauth_check = OAuth.objects.filter(openid=open_id).only('openid', 'user').first()
    if oauth_check:  # 已存在该用户，直接登录
        user = User.objects.get(id=oauth_check.user.id)
        if user.login_power == 1:
            request.session['user_name'] = user.user_name  # （将用户信息存入session）
            request.session['user_id'] = user.id
            request.session['user_authority'] = user.user_authority
            return HttpResponseRedirect('/')  # 回到主页
        else:
            info = '该用户无登录权限，请联系管理员解封'
            return HttpResponseRedirect(reverse('oauth:github_response', kwargs={'info': info}))  # 响应页面
    else:
        if email != '':
            user = User.objects.filter(email=email).only('id', 'user_name', 'user_authority', 'login_power').first()
            if user:  # 该邮箱对应的用户已经存在
                oauth_user = OAuth(openid=open_id, user_id=user.id, type=type)
                oauth_user.save()
                if user.login_power == 1:
                    request.session['user_name'] = user.user_name  # （将用户信息存入session）
                    request.session['user_id'] = user.id
                    request.session['user_authority'] = user.user_authority
                    return HttpResponseRedirect('/')  # 回到主页
                else:
                    info = '该用户无登录权限，请联系管理员解封'
                    return HttpResponseRedirect(reverse('oauth:github_response', kwargs={'info': info}))  # 相应页面
            else:  # 邮箱对应的用户不存在，将github信息和用户信息写入数据库
                if User.objects.filter(user_name=nickname):  # 用户名重复
                    nickname = 'CM-' + nickname
                img_path = upload_user_img(image_url)
                if User.objects.count() == 0:
                    user_o = User(user_img=img_path, user_name=nickname, password=make_password(nickname), email=email,
                                  user_authority=1, login_power=1, login_state=0)
                else:
                    user_o = User(user_img=img_path, user_name=nickname, password=make_password(nickname), email=email,
                                  user_authority=0, login_power=1, login_state=0)
                user_o.save()
                oauth_user = OAuth(openid=open_id, user_id=user_o.id, type=type)
                oauth_user.save()
                request.session['user_name'] = user_o.user_name
                request.session['user_id'] = user_o.id
                request.session['user_authority'] = user_o.user_authority
                info = '授权登录成功，初始密码为用户名'
                return HttpResponseRedirect(reverse('oauth:github_response', kwargs={'info': info}))  # 响应页面
        else:
            info = '你的github账号尚未绑定邮箱'
            return HttpResponseRedirect(reverse('oauth:github_response', kwargs={'info': info}))  # 响应页面


# 响应页面
def github_response(request, info):
    return render(request, 'oauth/response.html', {'info': info})


# 将图片保存至本地
def upload_user_img(img_url):
    folder_path = os.path.join(settings.BASE_DIR, 'media', 'user_img')  # 图片保存文件夹路径
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)  # 不存在，则创建
    try:
        img_name = '{}{}'.format(uuid.uuid4().hex, '.jpg')  # 生成文件名
        file_path = os.path.join(folder_path, img_name)
        urllib.request.urlretrieve(img_url, filename=file_path)
        return 'user_img/{img_name}'.format(img_name=img_name)
    except Exception as e:
        print(e)
        return None
