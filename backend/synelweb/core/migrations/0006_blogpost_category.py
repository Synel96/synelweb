from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_blogpost_description"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql=(
                        "ALTER TABLE core_blogpost "
                        "ADD COLUMN IF NOT EXISTS category varchar(20) "
                        "NOT NULL DEFAULT 'professional';"
                    ),
                    reverse_sql="ALTER TABLE core_blogpost DROP COLUMN IF EXISTS category;",
                ),
                migrations.RunSQL(
                    sql=(
                        "CREATE INDEX IF NOT EXISTS core_blogpost_category_idx "
                        "ON core_blogpost (category);"
                    ),
                    reverse_sql="DROP INDEX IF EXISTS core_blogpost_category_idx;",
                ),
            ],
            state_operations=[
                migrations.AddField(
                    model_name="blogpost",
                    name="category",
                    field=models.CharField(
                        choices=[("professional", "Szakmai"), ("casual", "Hetkoznapi")],
                        db_index=True,
                        default="professional",
                        help_text="Kategoria: szakmai vagy hetkoznapi",
                        max_length=20,
                    ),
                )
            ],
        ),
    ]
