from django.core.management.base import BaseCommand
from todo_app.models import Task
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Create sample tasks for testing'

    def handle(self, *args, **options):
        sample_tasks = [
            {
                'title': 'Finir le devoir de Django',
                'description': 'pour Samedi',
                'due_date': datetime.now().date() + timedelta(days=1),
                'completed': False
            },
            {
                'title': 'Changer le Css',
                'description': 'pour Samedi',
                'due_date': datetime.now().date(),
                'completed': True
            },
            {
                'title': 'changer Pycharm',
                'description': 'Il reste un seul jour en Trial',
                'due_date': datetime.now().date() + timedelta(days=7),
                'completed': False
            }
        ]

        for task_data in sample_tasks:
            task, created = Task.objects.get_or_create(
                title=task_data['title'],
                defaults=task_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Tache cree: {task.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'La tache existe deja: {task.title}')
                )