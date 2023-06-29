from celery import shared_task
from django.utils import timezone

from .models import Item


@shared_task
def check_expired_items():
    """
    Update the is_available field to False for all items with end_date in the past
    """
    now = timezone.now()
    expired_items = Item.objects.filter(end_date__lt=now, is_available=True)
    expired_items.update(is_available=False)
    print("Item available field updated!")
