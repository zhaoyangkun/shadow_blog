from django.contrib.sitemaps import Sitemap

from admin.models import Article, Category


class ArticleSitemap(Sitemap):
    changefreq = 'daily'  # 可选,指定每个对象的更新频率
    priority = 0.6  # 可选,指定每个对象的优先级,默认0.5

    def items(self):  # 返回对象的列表.这些对象将被其他方法或属性调用
        return Article.objects.filter(is_show=1).order_by('-gmt_created')

    def lastmod(self, obj):  # 可选,该方法返回一个datetime,表示每个对象的最后修改时间
        return obj.gmt_modified
