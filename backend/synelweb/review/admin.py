from django.contrib import admin

from core.deploy_hooks import trigger_vercel_deploy
from core.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
	list_display = ("name", "email", "rating", "is_approved", "created_at")
	search_fields = ("name", "email", "comment")
	list_filter = ("is_approved", "rating", "created_at")
	actions = ("approve_reviews",)
	readonly_fields = ("name", "email", "rating", "comment", "created_at")

	def has_add_permission(self, request):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

	@admin.action(description="Kijelölt vélemények jóváhagyása")
	def approve_reviews(self, request, queryset):
		# queryset.update() is a bulk UPDATE and does not fire the model's
		# post_save signal, so trigger the deploy hook explicitly here.
		newly_approved = queryset.filter(is_approved=False).count()
		queryset.update(is_approved=True)
		if newly_approved:
			trigger_vercel_deploy("reviews approved")
