from django.db import migrations

from blog.legacy_import import copy_legacy_posts


def forwards(apps, schema_editor):
    copy_legacy_posts(schema_editor.connection, apps.get_model("blog", "Article"))


class Migration(migrations.Migration):
    # Copies the old section-based posts (core_blogpost / core_blogsection)
    # into blog.Article. The old tables are only read. Undoing this leaves the
    # copied posts in place: nothing is deleted in either direction.

    dependencies = [
        ("blog", "0001_initial"),
        ("core", "0008_package_category_monthly_price"),
    ]

    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
