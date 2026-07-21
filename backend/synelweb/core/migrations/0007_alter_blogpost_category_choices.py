from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_blogpost_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogpost",
            name="category",
            field=models.CharField(
                choices=[
                    ("professional", "Szakmai"),
                    ("casual", "Hetkoznapi"),
                    ("dirty-financials", "Piszkos anyagiak"),
                ],
                db_index=True,
                default="professional",
                help_text="Kategoria: szakmai, hetkoznapi vagy piszkos anyagiak",
                max_length=20,
            ),
        ),
    ]
