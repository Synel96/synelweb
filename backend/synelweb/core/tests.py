from unittest import mock

from django.core.cache import cache
from django.test import TestCase, override_settings

from core.deploy_hooks import trigger_vercel_deploy
from core.models import BlogPost, Package, Review


@override_settings(VERCEL_DEPLOY_HOOK_URL="https://api.vercel.com/v1/integrations/deploy/test")
class TriggerVercelDeployTests(TestCase):
    def setUp(self):
        cache.clear()

    @mock.patch("core.deploy_hooks.requests.post")
    def test_posts_to_configured_hook_url(self, mock_post):
        with mock.patch("core.deploy_hooks.threading.Thread") as mock_thread:
            trigger_vercel_deploy("unit test")
            # run the target synchronously instead of spawning a real thread
            _, kwargs = mock_thread.call_args
            kwargs["target"](*kwargs["args"])

        mock_post.assert_called_once_with(
            "https://api.vercel.com/v1/integrations/deploy/test", timeout=10
        )

    @mock.patch("core.deploy_hooks.threading.Thread")
    def test_debounces_rapid_calls(self, mock_thread):
        trigger_vercel_deploy("first")
        trigger_vercel_deploy("second")

        self.assertEqual(mock_thread.call_count, 1)

    @override_settings(VERCEL_DEPLOY_HOOK_URL="")
    @mock.patch("core.deploy_hooks.threading.Thread")
    def test_noop_without_hook_url(self, mock_thread):
        trigger_vercel_deploy("no url configured")

        mock_thread.assert_not_called()


@override_settings(VERCEL_DEPLOY_HOOK_URL="https://api.vercel.com/v1/integrations/deploy/test")
class DeployHookSignalTests(TestCase):
    def setUp(self):
        cache.clear()

    @mock.patch("core.signals.trigger_vercel_deploy")
    def test_saving_a_package_triggers_deploy(self, mock_trigger):
        with self.captureOnCommitCallbacks(execute=True):
            Package.objects.create(name="Landing oldal", description="{}")

        mock_trigger.assert_called_once_with("service created")

    @mock.patch("core.signals.trigger_vercel_deploy")
    def test_saving_a_blog_post_triggers_deploy(self, mock_trigger):
        with self.captureOnCommitCallbacks(execute=True):
            BlogPost.objects.create(title="Elso poszt", description="Rovid leiras")

        mock_trigger.assert_called_once_with("blog post created")

    @mock.patch("core.signals.trigger_vercel_deploy")
    def test_approving_a_review_via_save_triggers_deploy(self, mock_trigger):
        review = Review.objects.create(name="Teszt Elek", rating=5)
        mock_trigger.reset_mock()

        with self.captureOnCommitCallbacks(execute=True):
            review.is_approved = True
            review.save()

        mock_trigger.assert_called_once_with("review approved")

    @mock.patch("core.signals.trigger_vercel_deploy")
    def test_unapproved_review_save_does_not_trigger_deploy(self, mock_trigger):
        with self.captureOnCommitCallbacks(execute=True):
            Review.objects.create(name="Teszt Elek", rating=5)

        mock_trigger.assert_not_called()
