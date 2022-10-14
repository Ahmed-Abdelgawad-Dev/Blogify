from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
from markdown import markdown


register = template.Library()
# STR
@register.simple_tag
def total_posts():
    return Post.published.count()

# RenderedTemplate
@register.inclusion_tag("blog/post/latest_posts.html")
# Count Parameter adds providing a parameter in the template
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {"latest_posts": latest_posts}

# Query Set
@register.simple_tag
def get_most_commented_posts(count=5):
    values = Post.published.annotate(
        total_comments=Count('comments')).order_by('-total_comments')[:count]
    return values




@register.filter(name='markdown')
def markdown_format(txt):
    return mark_safe(markdown(txt))