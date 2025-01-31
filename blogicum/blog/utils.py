from django.db.models import Count
from django.utils import timezone


def get_posts_queryset(objects_manager):
    return (
        objects_manager
        .filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True
        )
        .select_related('author')
        .prefetch_related('category', 'location')
        .order_by('-pub_date')
        .annotate(comment_count=Count('comments'))
    )


def get_user_posts(objects_manager):
    return (
        objects_manager
        .select_related('author')
        .prefetch_related('category', 'location')
        .order_by('-pub_date')
        .annotate(comment_count=Count('comments'))
    )
