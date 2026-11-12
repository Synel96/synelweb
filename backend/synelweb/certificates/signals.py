from django.db import transaction
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from core.deploy_hooks import trigger_vercel_deploy

from .models import Certificate


# The Certificates page is prerendered, so rebuild it when one changes.
@receiver(post_save, sender=Certificate)
def certificate_saved(sender, instance, created, **kwargs):
    reason = "certificate created" if created else "certificate updated"
    transaction.on_commit(lambda: trigger_vercel_deploy(reason))


@receiver(post_delete, sender=Certificate)
def certificate_deleted(sender, instance, **kwargs):
    transaction.on_commit(lambda: trigger_vercel_deploy("certificate deleted"))
