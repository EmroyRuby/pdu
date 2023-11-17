from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule


class Command(BaseCommand):
    help = 'Creates or updates a periodic task for sending event notifications'

    def handle(self, *args, **options):
        task_name = 'Send event notifications every 24 hours'

        # Check if the periodic task already exists
        existing_task = PeriodicTask.objects.filter(name=task_name).first()
        if existing_task:
            self.stdout.write(f'Deleting existing task with name "{task_name}"...')
            existing_task.delete()

        # Create a new schedule for every 1440 minutes (24 hours)
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=20,
            period=IntervalSchedule.MINUTES,
        )

        # Create the periodic task
        task = PeriodicTask.objects.create(
            interval=schedule,
            name=task_name,
            task='events.tasks.send_event_notifications',
        )

        self.stdout.write(self.style.SUCCESS(f'Successfully created periodic task: "{task.name}"'))
