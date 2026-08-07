from django.db import transaction
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .deploy_hooks import trigger_vercel_deploy
from .models import BlogPost, Package, Review


def _trigger_after_commit(reason):
    transaction.on_commit(lambda: trigger_vercel_deploy(reason))


@receiver(post_save, sender=Package)
def package_saved(sender, instance, created, **kwargs):
    _trigger_after_commit("service created" if created else "service updated")


@receiver(post_delete, sender=Package)
def package_deleted(sender, instance, **kwargs):
    _trigger_after_commit("service deleted")


@receiver(post_save, sender=BlogPost)
def blog_post_saved(sender, instance, created, **kwargs):
    _trigger_after_commit("blog post created" if created else "blog post updated")


@receiver(post_delete, sender=BlogPost)
def blog_post_deleted(sender, instance, **kwargs):
    _trigger_after_commit("blog post deleted")


@receiver(post_save, sender=Review)
def review_saved(sender, instance, created, **kwargs):
    # Covers editing a review's is_approved checkbox from the change form.
    # Bulk-approving via the admin action uses queryset.update(), which
    # bypasses this signal, so that action triggers the hook itself.
    if instance.is_approved:
        _trigger_after_commit("review approved")
