import time

from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.urls import reverse

from admin.models import User

try:
    from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
except ImportError:
    MiddlewareMixin = object  # Django 1.4.x - Django 1.9.x

'''
登录权限拦截器
'''


class SimpleMiddleware(MiddlewareMixin):

    def process_request(self, request):
        path = request.path
        # host = request.get_host()
        # redirect_url = "http://" + host + "/front/loginDis"
        full_path = request.get_full_path()
        port = request.get_port()
        # print("path: " + path + "\nhost: " + host + "\nport: " + port + "\nfull_path: " + full_path)
        if "/code" in path or "/static" in path or "/media" in path or "/front" in path or path == '/' or "/login" in path or "/register" in path:  # 合法路径
            pass
        elif "admin" in path:  # 校验用户是否登陆
            try:
                # 获取session中的用户信息
                user_name = request.session['user_name']
                user = User.objects.get(user_name=user_name)
                if user.login_power == 1:
                    if user.user_authority == 1:
                        pass
                    else:
                        return HttpResponseRedirect(reverse('response', kwargs={'error': '无权访问'}))
                else:
                    return HttpResponseRedirect(reverse('response', kwargs={'error': '无权访问'}))
            except KeyError:
                return HttpResponseRedirect(reverse('response', kwargs={'error': '无权访问'}))

    def process_response(self, request, response):
        # response['Access-Control-Allow-Origin'] = "*"
        # response['Access-Control-Allow-Headers'] = "Content-Type"
        # response['Access-Control-Allow-Method'] = "POST,GET,PUT,DELETE,PATCH"
        return response


'''
限制ip访问次数
'''
MAX_REQUEST_PER_SECOND = 2  # 每秒访问次数


class BlockMiddleware(MiddlewareMixin):

    def process_request(self, request):
        now = time.time()
        request_queue = request.session.get('request_queue', [])
        if len(request_queue) < MAX_REQUEST_PER_SECOND:
            request_queue.append(now)
            request.session['request_queue'] = request_queue
        else:
            time0 = request_queue[0]
            if (now - time0) < 1:
                time.sleep(2)
            request_queue.append(time.time())
            request.session['request_queue'] = request_queue[1:]

    def process_response(self, request, response):
        return response
