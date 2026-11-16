from django.db import transaction
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from core.deploy_hooks import trigger_vercel_deploy

from .models import Article


# Blog pages are prerendered, so rebuild the site when a post changes.
@receiver(post_save, sender=Article)
def article_saved(sender, instance, created, **kwargs):
    reason = "blog post created" if created else "blog post updated"
    transaction.on_commit(lambda: trigger_vercel_deploy(reason))


@receiver(post_delete, sender=Article)
def article_deleted(sender, instance, **kwargs):
    transaction.on_commit(lambda: trigger_vercel_deploy("blog post deleted"))
