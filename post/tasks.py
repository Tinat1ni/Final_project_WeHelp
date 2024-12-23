from celery import shared_task
from django.utils.timezone import now
from .models import Post
from django.db.models import Q

@shared_task
def delete_expired_posts():
    expired_or_completed_posts = Post.objects.filter(
        Q(deadline__lt=now()) | Q(completed=True)
    )
    count = expired_or_completed_posts.count()
    expired_or_completed_posts.delete()
    return f'{count} posts have been deleted'