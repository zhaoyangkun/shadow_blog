from admin.models import Site, User


# 模板全局信息
def base__info(request):
    site = Site.objects.all().defer('gmt_created', 'gmt_modified', 'remark').first()
    root_user = User.objects.filter(user_authority=1).only('user_img').first()
    return {'site': site, 'root_user': root_user}
