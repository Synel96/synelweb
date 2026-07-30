from django.core.management.base import BaseCommand

from packages.currency import fetch_rates


class Command(BaseCommand):
    help = "Refresh cached HUF exchange rates from frankfurter.app"

    def handle(self, *args, **options):
        rates = fetch_rates()
        self.stdout.write(self.style.SUCCESS(f"Updated exchange rates: {rates}"))
