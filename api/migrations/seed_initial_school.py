from django.db import migrations


def create_initial_school(apps, schema_editor):
    School = apps.get_model("api", "School")

    School.objects.get_or_create(
        code="DEFAULT",
        defaults={
            "name": "MORA School",
            "is_active": True,
        },
    )


def remove_initial_school(apps, schema_editor):
    School = apps.get_model("api", "School")
    School.objects.filter(code="DEFAULT").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("api", "00xx_previous_migration"),
    ]

    operations = [
        migrations.RunPython(
            create_initial_school,
            remove_initial_school,
        ),
    ]