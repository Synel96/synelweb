from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
import os


def project_media_upload_to(instance, filename):
    # A project neve alapján alkotjuk meg az elérési utat
    project_name = slugify(instance.project.name if hasattr(instance, "project") else instance.name)
    return os.path.join("projects", project_name, filename)


class Package(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)  # SEO-barát URL
    preview_image_url = models.URLField(
        max_length=500, blank=True,
        help_text="Kép URL-je (pl. https://példa.hu/kep.png)"
    )
    description = models.TextField()
    is_discounted = models.BooleanField(default=False, db_index=True)  # gyors szűrés
    tags = models.CharField(
        max_length=255, blank=True,
        help_text="Vesszővel elválasztva: pl. seo, statikus oldal, pwa"
    )
    created_at = models.DateTimeField(auto_now_add=True)  # jól jön listázásnál
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name

    @property
    def tags_list(self):
        return [t.strip() for t in self.tags.split(",") if t.strip()]

    def save(self, *args, **kwargs):
        # slug automatikus és egyedi generálása
        if not self.slug:
            base = slugify(self.name)[:110]
            slug = base
            i = 1
            Model = type(self)
            while Model.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)


class Review(models.Model):
    name = models.CharField(max_length=100)  # kötelező
    email = models.EmailField(blank=True, null=True)  # opcionális
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )  # 0–5 kötelező
    comment = models.TextField(blank=True, null=True)  # opcionális
    is_approved = models.BooleanField(default=False, help_text="Jóváhagyás után jelenjen meg")  # moderáció
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.rating}★)"


class Project(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    project_type = models.CharField(max_length=100, db_index=True)
    description = models.TextField(blank=True, help_text="Projekt részletes leírása")  # ÚJ mező
    preview_video = models.FileField(
        upload_to=project_media_upload_to, blank=True, null=True,
        help_text="Projekt bemutató videó (pl. mp4)"
    )
    preview_image = models.ImageField(
        upload_to=project_media_upload_to, blank=True, null=True,
        help_text="Előnézeti kép"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)[:210]
            slug = base
            i = 1
            Model = type(self)
            while Model.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)


class ProjectImage(models.Model):
    """További képek egy projekthez"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="extra_images")
    image = models.ImageField(upload_to=project_media_upload_to, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        constraints = [
            models.UniqueConstraint(fields=["project", "order"], name="uniq_project_order")
        ]

    def image_url(self):
        if self.image:
            return self.image.url
        return ""
    image_url.short_description = "Kép URL"

    def __str__(self):
        return f"{self.project.name} - kép {self.order}"
