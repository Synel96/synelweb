# Written by hand on purpose: `makemigrations core` would also pick up an
# older, unrelated pending change (NewsParagraph) that needs its own review.
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0007_alter_blogpost_category_choices"),
    ]

    operations = [
        migrations.AddField(
            model_name="package",
            name="category",
            field=models.CharField(
                choices=[
                    ("website", "Weboldal-fejlesztés"),
                    ("marketing", "Láthatóság és marketing"),
                    ("operations", "Üzemeltetés és kiegészítők"),
                ],
                db_index=True,
                default="website",
                help_text="Melyik blokkban jelenjen meg a Szolgáltatások oldalon.",
                max_length=12,
                verbose_name="Kategória",
            ),
        ),
        migrations.AddField(
            model_name="package",
            name="monthly_price",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text=(
                    "Havi díj Ft-ban, ha van (pl. hirdetéskezelés: kezelés, konfigurálás, "
                    "elemzés). Ilyenkor a normál ár az egyszeri beállítási díj."
                ),
                max_digits=10,
                null=True,
                verbose_name="Havi díj",
            ),
        ),
    ]
