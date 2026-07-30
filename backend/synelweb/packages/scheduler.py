import logging

logger = logging.getLogger(__name__)

_started = False


def start():
    """Start the daily exchange-rate refresh job (idempotent, safe to call once per process)."""
    global _started
    if _started:
        return
    _started = True

    try:
        from apscheduler.schedulers.background import BackgroundScheduler
    except ImportError:
        logger.warning("apscheduler is not installed; exchange rate auto-refresh is disabled")
        return

    from django.core.management import call_command

    def refresh_job():
        try:
            call_command("update_exchange_rates")
        except Exception:
            logger.exception("Scheduled exchange rate refresh failed")

    scheduler = BackgroundScheduler(daemon=True, timezone="UTC")
    scheduler.add_job(
        refresh_job, "cron", hour=3, minute=0,
        id="update_exchange_rates", replace_existing=True,
    )
    scheduler.start()
    logger.info("Exchange rate scheduler started (daily at 03:00 UTC)")
