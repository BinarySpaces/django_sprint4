from django.db.models import Count
from django.utils import timezone

from . models import Post


def get_posts(posts=Post.objects,
              only_published=True,
              select_related_fields=True,
              annotate_comments=True):

    if only_published:
        posts = posts.filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True
        )

    if select_related_fields:
        posts = posts.select_related('author', 'category', 'location')

    if annotate_comments:
        posts = posts.annotate(
            comment_count=Count('comments')
        ).order_by(*Post._meta.ordering)

    return posts
