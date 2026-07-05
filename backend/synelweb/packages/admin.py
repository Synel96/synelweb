import json

from django import forms
from django.contrib import admin
from django.utils.html import format_html

from core.models import Package


class PackageAdminForm(forms.ModelForm):
	title_hu = forms.CharField(label="Title (HU)", required=False)
	title_en = forms.CharField(label="Title (EN)", required=False)
	title_de = forms.CharField(label="Title (DE)", required=False)
	slug_hu = forms.CharField(label="Slug (HU)", required=False)
	slug_en = forms.CharField(label="Slug (EN)", required=False)
	slug_de = forms.CharField(label="Slug (DE)", required=False)
	description_hu = forms.CharField(label="Description (HU)", required=False, widget=forms.Textarea)
	description_en = forms.CharField(label="Description (EN)", required=False, widget=forms.Textarea)
	description_de = forms.CharField(label="Description (DE)", required=False, widget=forms.Textarea)
	is_active = forms.BooleanField(label="Active", required=False, initial=True)
	display_order = forms.IntegerField(label="Order", required=False, min_value=0)

	class Meta:
		model = Package
		fields = [
			"preview_image_url",
			"is_discounted",
			"price",
			"discounted_price",
			"tags",
		]

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		payload = None
		instance = self.instance
		if instance and instance.pk:
			self.fields["title_hu"].initial = instance.name
			self.fields["title_en"].initial = instance.name
			self.fields["title_de"].initial = instance.name
			self.fields["slug_hu"].initial = instance.slug
			self.fields["slug_en"].initial = instance.slug
			self.fields["slug_de"].initial = instance.slug
			try:
				parsed = json.loads((instance.description or "").strip())
				if isinstance(parsed, dict):
					payload = parsed
			except (TypeError, ValueError, json.JSONDecodeError):
				payload = None
		if payload:
			title = payload.get("title") if isinstance(payload.get("title"), dict) else {}
			slug = payload.get("slug") if isinstance(payload.get("slug"), dict) else {}
			desc = payload.get("description") if isinstance(payload.get("description"), dict) else {}
			self.fields["title_hu"].initial = title.get("hu", self.fields["title_hu"].initial)
			self.fields["title_en"].initial = title.get("en", self.fields["title_en"].initial)
			self.fields["title_de"].initial = title.get("de", self.fields["title_de"].initial)
			self.fields["slug_hu"].initial = slug.get("hu", self.fields["slug_hu"].initial)
			self.fields["slug_en"].initial = slug.get("en", self.fields["slug_en"].initial)
			self.fields["slug_de"].initial = slug.get("de", self.fields["slug_de"].initial)
			self.fields["description_hu"].initial = desc.get("hu", "")
			self.fields["description_en"].initial = desc.get("en", "")
			self.fields["description_de"].initial = desc.get("de", "")
			if isinstance(payload.get("isActive"), bool):
				self.fields["is_active"].initial = payload["isActive"]
			if isinstance(payload.get("order"), int):
				self.fields["display_order"].initial = payload["order"]
		elif instance and instance.pk:
			self.fields["description_hu"].initial = instance.description
			self.fields["description_en"].initial = instance.description
			self.fields["description_de"].initial = instance.description

	def save(self, commit=True):
		instance = super().save(commit=False)
		hu_title = (self.cleaned_data.get("title_hu") or "").strip()
		hu_slug = (self.cleaned_data.get("slug_hu") or "").strip()
		instance.name = hu_title or instance.name
		instance.slug = hu_slug or instance.slug
		payload = {
			"title": {
				"hu": hu_title,
				"en": (self.cleaned_data.get("title_en") or hu_title).strip(),
				"de": (self.cleaned_data.get("title_de") or hu_title).strip(),
			},
			"slug": {
				"hu": hu_slug,
				"en": (self.cleaned_data.get("slug_en") or hu_slug).strip(),
				"de": (self.cleaned_data.get("slug_de") or hu_slug).strip(),
			},
			"description": {
				"hu": (self.cleaned_data.get("description_hu") or "").strip(),
				"en": (self.cleaned_data.get("description_en") or "").strip(),
				"de": (self.cleaned_data.get("description_de") or "").strip(),
			},
			"isActive": bool(self.cleaned_data.get("is_active")),
			"order": self.cleaned_data.get("display_order") if self.cleaned_data.get("display_order") is not None else (instance.id or 0),
		}
		instance.description = json.dumps(payload, ensure_ascii=False)
		if commit:
			instance.save()
			self.save_m2m()
		return instance


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
	form = PackageAdminForm
	list_display = ("name", "image_tag", "is_discounted", "price", "discounted_price", "created_at")
	search_fields = ("name", "slug", "tags")
	list_filter = ("is_discounted", "created_at")

	def image_tag(self, obj):
		if obj.preview_image_url:
			return format_html('<img src="{}" style="max-height: 60px; max-width: 100px;" />', obj.preview_image_url)
		return "-"

	image_tag.short_description = "Kép"
