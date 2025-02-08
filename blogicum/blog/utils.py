from django.db.models import Count
from django.utils import timezone

from . models import Post


def get_posts(posts=Post.objects,
              user=None,
              filter_posts=True,
              select_related_fields=True,
              use_model_ordering=True,
              annotate_comments=True):

    if filter_posts:
        posts = posts.filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True
        )

    if select_related_fields:
        posts = posts.select_related('author', 'category', 'location')

    if use_model_ordering:
        ordering = Post._meta.ordering
        if ordering:
            posts = posts.order_by(*ordering)

    if annotate_comments:
        posts = posts.annotate(comment_count=Count('comments'))

    return posts
