from django.core.management.base import BaseCommand, CommandError

from api.models import School


class Command(BaseCommand):
    help = "Create the initial school configuration."

    def handle(self, *args, **options):

        school_count = School.objects.count()

        if school_count > 1:
            raise CommandError(
                "MORA must contain only one School record."
            )

        if school_count == 1:
            school = School.objects.first()

            self.stdout.write(
                self.style.WARNING(
                    f"School already exists: {school.name} ({school.code})"
                )
            )

            return

        school = School.objects.create(
            name="MAN 2 PONTIANAK",
            code="MAN2PNK",
            is_active=True,
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Initial school created: {school.name} ({school.code})"
            )
        )