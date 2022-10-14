from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    
    def items(self):
        posts = Post.published.all()
        return posts

    def lastmod(self, item):
        return item.updated
    