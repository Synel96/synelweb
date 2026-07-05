from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_blogpost_blogsection"),
    ]

    operations = [
        migrations.AddField(
            model_name="blogpost",
            name="description",
            field=models.TextField(
                blank=True,
                help_text="Rövid leírás a blogposzthoz (pl. listanézethez)",
                default="",
            ),
            preserve_default=False,
        ),
    ]
