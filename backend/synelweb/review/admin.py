from django.contrib import admin

from core.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
	list_display = ("name", "email", "rating", "is_approved", "created_at")
	search_fields = ("name", "email", "comment")
	list_filter = ("is_approved", "rating", "created_at")
	actions = ("approve_reviews", "disapprove_reviews")

	@admin.action(description="Kijelölt vélemények jóváhagyása")
	def approve_reviews(self, request, queryset):
		queryset.update(is_approved=True)

	@admin.action(description="Kijelölt vélemények jóváhagyásának visszavonása")
	def disapprove_reviews(self, request, queryset):
		queryset.update(is_approved=False)
