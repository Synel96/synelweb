import json

from django import forms
from django.contrib import admin
from django.utils.html import format_html

from core.models import Project, ProjectImage


class ProjectImageInline(admin.TabularInline):
	model = ProjectImage
	extra = 1


class ProjectAdminForm(forms.ModelForm):
	description_hu = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 4}))
	description_en = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 4}))
	description_de = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 4}))
	stack_json = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 6}))
	lighthouse_mobile_json = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 6}))
	lighthouse_desktop_json = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 6}))
	live_url = forms.URLField(required=False)
	is_active = forms.BooleanField(required=False, initial=True)
	api_order = forms.IntegerField(required=False, min_value=0)

	class Meta:
		model = Project
		fields = "__all__"

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		payload = self._get_payload()
		description = payload.get("description", {})
		if isinstance(description, dict):
			self.fields["description_hu"].initial = description.get("hu", "")
			self.fields["description_en"].initial = description.get("en", "")
			self.fields["description_de"].initial = description.get("de", "")
		self.fields["stack_json"].initial = self._pretty_json(payload.get("stack", []))
		self.fields["lighthouse_mobile_json"].initial = self._pretty_json(payload.get("lighthouseMobile", []))
		self.fields["lighthouse_desktop_json"].initial = self._pretty_json(payload.get("lighthouseDesktop", []))
		self.fields["live_url"].initial = payload.get("liveUrl", "")
		self.fields["is_active"].initial = payload.get("isActive", True)
		self.fields["api_order"].initial = payload.get("order")

	def _get_payload(self):
		raw = (self.instance.description or "").strip()
		if not raw.startswith("{"):
			return {}
		try:
			parsed = json.loads(raw)
			if isinstance(parsed, dict):
				return parsed
		except (TypeError, ValueError, json.JSONDecodeError):
			pass
		return {}

	def _pretty_json(self, value):
		if not value:
			return ""
		return json.dumps(value, ensure_ascii=False, indent=2)

	def clean_stack_json(self):
		return self._clean_json_field("stack_json", expect=list)

	def clean_lighthouse_mobile_json(self):
		value = self._clean_json_field("lighthouse_mobile_json", expect=list)
		self._validate_lighthouse(value, "lighthouse_mobile_json")
		return value

	def clean_lighthouse_desktop_json(self):
		value = self._clean_json_field("lighthouse_desktop_json", expect=list)
		self._validate_lighthouse(value, "lighthouse_desktop_json")
		return value

	def _clean_json_field(self, field_name, expect):
		raw = (self.cleaned_data.get(field_name) or "").strip()
		if not raw:
			return [] if expect is list else {}
		try:
			parsed = json.loads(raw)
		except json.JSONDecodeError as exc:
			raise forms.ValidationError(f"Invalid JSON in {field_name}: {exc}") from exc
		if not isinstance(parsed, expect):
			expected_name = "array" if expect is list else "object"
			raise forms.ValidationError(f"{field_name} must be a JSON {expected_name}.")
		return parsed

	def _validate_lighthouse(self, value, field_name):
		if not value:
			return
		required_labels = {"performance", "accessibility", "bestPractices", "seo"}
		labels = set()
		for item in value:
			if not isinstance(item, dict):
				raise forms.ValidationError(f"{field_name} items must be objects.")
			label = item.get("label")
			raw_value = item.get("value")
			if label not in required_labels:
				raise forms.ValidationError(f"{field_name} has invalid label: {label}")
			if not isinstance(raw_value, int) or raw_value < 0 or raw_value > 100:
				raise forms.ValidationError(f"{field_name} value must be an integer between 0 and 100.")
			labels.add(label)
		if labels != required_labels:
			raise forms.ValidationError(f"{field_name} must contain exactly: performance, accessibility, bestPractices, seo")

	def save(self, commit=True):
		instance = super().save(commit=False)
		payload = {
			"description": {
				"hu": (self.cleaned_data.get("description_hu") or "").strip(),
				"en": (self.cleaned_data.get("description_en") or "").strip(),
				"de": (self.cleaned_data.get("description_de") or "").strip(),
			},
			"stack": self.cleaned_data.get("stack_json") or [],
			"lighthouseMobile": self.cleaned_data.get("lighthouse_mobile_json") or [],
			"lighthouseDesktop": self.cleaned_data.get("lighthouse_desktop_json") or [],
			"liveUrl": (self.cleaned_data.get("live_url") or "").strip(),
			"isActive": bool(self.cleaned_data.get("is_active", True)),
			"order": self.cleaned_data.get("api_order"),
		}
		instance.description = json.dumps(payload, ensure_ascii=False)
		if commit:
			instance.save()
			self.save_m2m()
		return instance


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
	form = ProjectAdminForm
	list_display = ("name", "project_type", "preview_tag", "created_at")
	search_fields = ("name", "slug", "project_type")
	prepopulated_fields = {"slug": ("name",)}
	inlines = [ProjectImageInline]
	fieldsets = (
		("Alap", {"fields": ("name", "slug", "project_type", "preview_image", "preview_video")}),
		("Többnyelvű leírás", {"fields": ("description_hu", "description_en", "description_de")}),
		("Frontend mezők (JSON)", {"fields": ("stack_json", "lighthouse_mobile_json", "lighthouse_desktop_json")}),
		("Frontend meta", {"fields": ("live_url", "is_active", "api_order")}),
	)

	def preview_tag(self, obj):
		if obj.preview_image:
			return format_html('<img src="{}" style="max-height: 60px; max-width: 100px;" />', obj.preview_image.url)
		return "-"

	preview_tag.short_description = "Előnézet"


@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
	list_display = ("project", "image_tag", "order")
	search_fields = ("project__name",)
	list_filter = ("project",)

	def image_tag(self, obj):
		if obj.image:
			return format_html('<img src="{}" style="max-height: 60px; max-width: 100px;" />', obj.image.url)
		return "-"

	image_tag.short_description = "Kép"
