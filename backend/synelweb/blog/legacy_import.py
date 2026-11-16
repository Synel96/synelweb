"""One-off copy of the old section-based posts into blog.Article.

The old tables (core_blogpost, core_blogsection) are read with plain SQL and
left untouched: they stay as the backup of what the posts looked like.
"""

from .markdown_sections import join_sections

POST_TABLE = "core_blogpost"
SECTION_TABLE = "core_blogsection"


def copy_legacy_posts(connection, Article):
    """Create an Article for every old post that has none yet; return the count."""
    tables = set(connection.introspection.table_names())
    if POST_TABLE not in tables:
        return 0

    quote = connection.ops.quote_name
    with connection.cursor() as cursor:
        columns = {
            column.name for column in connection.introspection.get_table_description(cursor, POST_TABLE)
        }
        optional = [name for name in ("description", "category", "preview_image", "updated_at") if name in columns]
        selected = ["id", "title", "slug", "created_at", *optional]
        cursor.execute(f"SELECT {', '.join(quote(name) for name in selected)} FROM {quote(POST_TABLE)}")
        posts = [dict(zip(selected, row)) for row in cursor.fetchall()]

        sections = {}
        if SECTION_TABLE in tables:
            cursor.execute(
                f"SELECT {quote('blog_id')}, {quote('subtitle')}, {quote('content')} "
                f"FROM {quote(SECTION_TABLE)} ORDER BY {quote('blog_id')}, {quote('order')}, {quote('id')}"
            )
            for blog_id, subtitle, content in cursor.fetchall():
                sections.setdefault(blog_id, []).append((subtitle, content))

    existing = set(Article.objects.values_list("id", flat=True))
    taken_slugs = set(Article.objects.values_list("slug", flat=True))
    created = 0
    for post in posts:
        if post["id"] in existing:
            continue
        slug = post["slug"] or f"poszt-{post['id']}"
        if slug in taken_slugs:
            slug = f"{slug}-{post['id']}"
        taken_slugs.add(slug)

        Article.objects.bulk_create(
            [
                Article(
                    # Same id as before, so nothing that refers to a post by
                    # number changes.
                    id=post["id"],
                    slug=slug,
                    category=post.get("category") or "professional",
                    preview_image=post.get("preview_image") or None,
                    title_hu=post["title"],
                    description_hu=post.get("description") or "",
                    body_hu=join_sections(sections.get(post["id"], [])),
                    created_at=post["created_at"],
                )
            ]
        )
        # auto_now stamps "now" on creation; put the real date back.
        if post.get("updated_at"):
            Article.objects.filter(id=post["id"]).update(updated_at=post["updated_at"])
        created += 1

    if created and connection.vendor == "postgresql":
        # Explicit ids don't advance the id sequence; move it past them.
        table = Article._meta.db_table
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT setval(pg_get_serial_sequence(%s, 'id'), "
                f"(SELECT COALESCE(MAX(id), 1) FROM {quote(table)}))",
                [table],
            )
    return created
