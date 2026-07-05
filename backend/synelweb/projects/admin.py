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
	stack_plain = forms.CharField(
		required=False,
		widget=forms.Textarea(attrs={"rows": 6}),
		help_text="Soronkent: Tech Name|logo_key, pl: React|react",
	)
	lh_mobile_performance = forms.IntegerField(required=False, min_value=0, max_value=100)
	lh_mobile_accessibility = forms.IntegerField(required=False, min_value=0, max_value=100)
	lh_mobile_best_practices = forms.IntegerField(required=False, min_value=0, max_value=100)
	lh_mobile_seo = forms.IntegerField(required=False, min_value=0, max_value=100)
	lh_desktop_performance = forms.IntegerField(required=False, min_value=0, max_value=100)
	lh_desktop_accessibility = forms.IntegerField(required=False, min_value=0, max_value=100)
	lh_desktop_best_practices = forms.IntegerField(required=False, min_value=0, max_value=100)
	lh_desktop_seo = forms.IntegerField(required=False, min_value=0, max_value=100)
	live_url = forms.URLField(required=False)
	is_active = forms.BooleanField(required=False, initial=True)
	api_order = forms.IntegerField(required=False, min_value=0)

	DEFAULT_STACK = [
		{"name": "React", "logo": "react"},
		{"name": "TailwindCSS", "logo": "tailwind"},
		{"name": "TypeScript", "logo": "typescript"},
		{"name": "Python", "logo": "python"},
		{"name": "Django", "logo": "django"},
		{"name": "PostgreSQL", "logo": "postgresql"},
	]
	DEFAULT_LIGHTHOUSE = {
		"performance": 100,
		"accessibility": 100,
		"bestPractices": 100,
		"seo": 100,
	}

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
		stack = payload.get("stack") if isinstance(payload.get("stack"), list) else self.DEFAULT_STACK
		self.fields["stack_plain"].initial = self._stack_to_plain(stack)

		mobile = self._lighthouse_to_map(payload.get("lighthouseMobile"), self.DEFAULT_LIGHTHOUSE)
		desktop = self._lighthouse_to_map(payload.get("lighthouseDesktop"), self.DEFAULT_LIGHTHOUSE)
		self.fields["lh_mobile_performance"].initial = mobile["performance"]
		self.fields["lh_mobile_accessibility"].initial = mobile["accessibility"]
		self.fields["lh_mobile_best_practices"].initial = mobile["bestPractices"]
		self.fields["lh_mobile_seo"].initial = mobile["seo"]
		self.fields["lh_desktop_performance"].initial = desktop["performance"]
		self.fields["lh_desktop_accessibility"].initial = desktop["accessibility"]
		self.fields["lh_desktop_best_practices"].initial = desktop["bestPractices"]
		self.fields["lh_desktop_seo"].initial = desktop["seo"]

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

	def _stack_to_plain(self, stack_items):
		lines = []
		for item in stack_items:
			if not isinstance(item, dict):
				continue
			name = (item.get("name") or "").strip()
			logo = (item.get("logo") or "").strip()
			if name and logo:
				lines.append(f"{name}|{logo}")
		return "\n".join(lines)

	def _lighthouse_to_map(self, value, fallback):
		result = dict(fallback)
		if not isinstance(value, list):
			return result
		for item in value:
			if not isinstance(item, dict):
				continue
			label = item.get("label")
			raw_value = item.get("value")
			if label in result and isinstance(raw_value, int) and 0 <= raw_value <= 100:
				result[label] = raw_value
		return result

	def clean_stack_plain(self):
		raw = (self.cleaned_data.get("stack_plain") or "").strip()
		if not raw:
			raise forms.ValidationError("Adj meg legalabb 1 stack sort (name|logo).")
		stack = []
		for i, line in enumerate(raw.splitlines(), start=1):
			text = line.strip()
			if not text:
				continue
			if "|" not in text:
				raise forms.ValidationError(f"Hibas stack sor #{i}. Formatum: Name|logo")
			name, logo = text.split("|", 1)
			name = name.strip()
			logo = logo.strip()
			if not name or not logo:
				raise forms.ValidationError(f"Hibas stack sor #{i}. A name es logo kotelezo.")
			stack.append({"name": name, "logo": logo})
		if not stack:
			raise forms.ValidationError("Adj meg legalabb 1 stack elemet.")
		return stack

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

	def _build_lighthouse(self, prefix):
		return [
			{"label": "performance", "value": int(self.cleaned_data.get(f"{prefix}_performance"))},
			{"label": "accessibility", "value": int(self.cleaned_data.get(f"{prefix}_accessibility"))},
			{"label": "bestPractices", "value": int(self.cleaned_data.get(f"{prefix}_best_practices"))},
			{"label": "seo", "value": int(self.cleaned_data.get(f"{prefix}_seo"))},
		]

	def clean(self):
		cleaned = super().clean()
		for key in [
			"lh_mobile_performance",
			"lh_mobile_accessibility",
			"lh_mobile_best_practices",
			"lh_mobile_seo",
			"lh_desktop_performance",
			"lh_desktop_accessibility",
			"lh_desktop_best_practices",
			"lh_desktop_seo",
		]:
			if cleaned.get(key) is None:
				self.add_error(key, "Kotelezo mezo")
		return cleaned

	def save(self, commit=True):
		instance = super().save(commit=False)
		payload = {
			"description": {
				"hu": (self.cleaned_data.get("description_hu") or "").strip(),
				"en": (self.cleaned_data.get("description_en") or "").strip(),
				"de": (self.cleaned_data.get("description_de") or "").strip(),
			},
			"stack": self.cleaned_data.get("stack_plain") or [],
			"lighthouseMobile": self._build_lighthouse("lh_mobile"),
			"lighthouseDesktop": self._build_lighthouse("lh_desktop"),
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
		("Stack", {"fields": ("stack_plain",)}),
		(
			"Lighthouse Mobile",
			{"fields": ("lh_mobile_performance", "lh_mobile_accessibility", "lh_mobile_best_practices", "lh_mobile_seo")},
		),
		(
			"Lighthouse Desktop",
			{"fields": ("lh_desktop_performance", "lh_desktop_accessibility", "lh_desktop_best_practices", "lh_desktop_seo")},
		),
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
