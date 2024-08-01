from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create default users with specific roles'

    def handle(self, *args, **kwargs):
        users = [
            {'username': 'admin', 'password': 'admin123', 'role': 'admin'},
            {'username': 'institution', 'password': 'inst123', 'role': 'financial_institution'},
            {'username': 'gov_agency', 'password': 'gov123', 'role': 'government_agency'},
            {'username': 'logistics', 'password': 'log123', 'role': 'logistics_provider'},
        ]

        for user_data in users:
            if not User.objects.filter(username=user_data['username']).exists():
                User.objects.create_user(**user_data)
                self.stdout.write(self.style.SUCCESS(f"User '{user_data['username']}' created successfully"))
