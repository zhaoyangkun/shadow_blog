# shadow_blog

## 介绍

shadow_blog是一款基于Django的极简主义个人博客，已应用在[苍茫误此生博客](https://www.cangmangai.cn/)

前端基于[Boundless-UI](https://github.com/zhaoyangkun/Boundless-UI)，风格简约。支持响应式布局，
已适配主流的安卓和苹果设备。

后台功能不是很丰富，后期如果有时间会做功能的完善和补充。

## 前端功能

### 1.注册和登录：
支持github授权登录，和异步邮箱验证码注册。

### 2. 文章关键字模糊搜索、代码块markdown渲染

### 3. 文章分类、标签墙、归档、评论以及友情链接
评论区支持表情和markdown渲染。

### 4. 更改用户头像、呢称等个人信息

### 5. 文章浏览数和评论数统计，最热文章和猜你喜欢栏目



## 后端功能
包含基本的服务器端分页、模糊搜索功能。

### 1.用户管理
支持修改密码，锁定/启用账户，删除账户等功能。

### 2. 分类、标签墙管理
添加分类和标签，分类和标签相对应

### 3. 文章管理
可以通过markdown编辑器添加、修改文章，并添加标签和分诶，markdown编辑器支持多图片上传。

### 4. 评论管理

### 5. 友链管理

### 6. 修改站点信息
修改站点logo，站点名称，关键词，描述等信息。

### 7. 站点地图
默认启动站点地图功能,暂时不支持后台配置，可以通过域名 + sitemap.xml访问站点地图


## 使用说明

- 本项目依赖于python,pip和redis环境，请先配置好这些环境。python版本最好选择3.5以上的。

- 克隆项目至本地，创建虚拟环境（不创建也可以），再进入项目根目录，执行命令
pip install -r requirements.txt安装环境依赖，继续依次执行python manage.py makemigrations和
python manage.py migrate生成数据库。

- 在项目根目录执行python manage.py runserver 127.0.0.1:8000，使项目运行起来。

- 在项目根目录执行celery -A celery_tasks worker -l info -P eventlet启动celery任务。

- 在浏览器中访问127.0.0.1:8000，默认第一个注册用户或者第一个用github授权登录用户为管理员。

- 用刚刚注册的用户登录，登录之后在首页将鼠标移到右上方的用户名可以看到后台管理，进入即可。或者在登录之后手动
输入127.0.0.1:8000/admin进入后台管理。

## 部分功能截图