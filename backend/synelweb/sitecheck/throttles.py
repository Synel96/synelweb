"""Limits on the free website checker.

Every check that isn't cached runs a Google Lighthouse test (slow, counted
against the API quota) and fetches the checked site, so it is limited from
several sides: per visitor in a minute, an hour and a day, and for the whole
site in a day. Rates are in settings (REST_FRAMEWORK DEFAULT_THROTTLE_RATES).
"""

from rest_framework.throttling import SimpleRateThrottle


class _PerVisitorThrottle(SimpleRateThrottle):
    def get_cache_key(self, request, view):
        return self.cache_format % {"scope": self.scope, "ident": self.get_ident(request)}


class SiteCheckBurstThrottle(_PerVisitorThrottle):
    """A few checks in a row are fine (mobile + desktop, a typo); a script is not."""

    scope = "site_checks_burst"


class SiteCheckHourlyThrottle(_PerVisitorThrottle):
    scope = "site_checks"


class SiteCheckDailyThrottle(_PerVisitorThrottle):
    scope = "site_checks_daily"


class SiteCheckGlobalThrottle(SimpleRateThrottle):
    """All visitors together: a ceiling for a flood from many addresses."""

    scope = "site_checks_global"

    def get_cache_key(self, request, view):
        return self.cache_format % {"scope": self.scope, "ident": "all"}
