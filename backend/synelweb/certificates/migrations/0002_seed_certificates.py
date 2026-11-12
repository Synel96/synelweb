import datetime
from decimal import Decimal

from django.db import migrations

CERTIFICATES = [
    {
        "title": "Google Ads Search Certification",
        "issuer": "Google Skillshop",
        "category": "marketing",
        "kind": "exam",
        "issued_on": datetime.date(2026, 11, 8),
        "expires_on": datetime.date(2027, 11, 8),
        "credential_url": "https://skillshop.credential.net/8c90725b-197e-4762-a876-7dbd88e09357",
        "credential_id": "199772599",
        "skills": "Google Ads, Search Ads, Keywords",
        "order": 0,
    },
    {
        "title": "PCEP™ – Certified Entry-Level Python Programmer",
        "issuer": "Python Institute (OpenEDG)",
        "category": "backend",
        "kind": "exam",
        "issued_on": datetime.date(2025, 5, 13),
        "credential_url": "https://verify.openedg.org/?id=U8ey.juhf.PKeC",
        "credential_id": "U8ey.juhf.PKeC",
        "skills": "Python, PCEP-30-02",
        "order": 0,
    },
    {
        "title": "Build a Backend REST API with Python & Django – Beginner",
        "issuer": "Udemy · Mark Winterbottom, Brooke Rutherford",
        "category": "backend",
        "kind": "course",
        "issued_on": datetime.date(2025, 5, 26),
        "hours": Decimal("5"),
        "credential_url": "https://ude.my/UC-809addf9-a80e-4067-9810-509ea371b337",
        "credential_id": "UC-809addf9-a80e-4067-9810-509ea371b337",
        "skills": "Python, Django, REST API",
        "order": 1,
    },
    {
        "title": "Become a Full-Stack Developer: React, Django REST, and MySQL",
        "issuer": "Udemy · Marek Adamovič",
        "category": "fullstack",
        "kind": "course",
        "issued_on": datetime.date(2025, 7, 8),
        "hours": Decimal("7.5"),
        "credential_url": "https://ude.my/UC-4b741a7d-9c97-4d24-8e11-250d914433fd",
        "credential_id": "UC-4b741a7d-9c97-4d24-8e11-250d914433fd",
        "skills": "React, Django REST, MySQL",
        "order": 0,
    },
    {
        "title": "Django with React | An Ecommerce Website",
        "issuer": "Udemy · Dennis Ivy, Brad Traversy",
        "category": "fullstack",
        "kind": "course",
        "issued_on": datetime.date(2026, 11, 9),
        "hours": Decimal("18"),
        "credential_url": "https://ude.my/UC-6e565ba3-506d-4e82-b521-e770c470be64",
        "credential_id": "UC-6e565ba3-506d-4e82-b521-e770c470be64",
        "skills": "Django, React, E-commerce",
        "order": 0,
    },
]


def seed(apps, schema_editor):
    Certificate = apps.get_model("certificates", "Certificate")
    for data in CERTIFICATES:
        Certificate.objects.update_or_create(
            title=data["title"], issuer=data["issuer"], defaults=data
        )


def unseed(apps, schema_editor):
    Certificate = apps.get_model("certificates", "Certificate")
    for data in CERTIFICATES:
        Certificate.objects.filter(title=data["title"], issuer=data["issuer"]).delete()


class Migration(migrations.Migration):
    dependencies = [("certificates", "0001_initial")]

    operations = [migrations.RunPython(seed, unseed)]
