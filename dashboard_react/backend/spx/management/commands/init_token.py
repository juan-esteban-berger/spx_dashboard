from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import os

class Command(BaseCommand):
    help = 'Initialize API token from environment'

    def handle(self, *args, **kwargs):
        # Create a default user if none exists
        if not User.objects.filter(username='api').exists():
            user = User.objects.create_user('api', 'api@example.com', 'api')
        else:
            user = User.objects.get(username='api')

        # Get token from environment
        env_token = os.getenv('API_TOKEN')
        
        if env_token:
            try:
                # Try to get existing token
                token = Token.objects.get(key=env_token)
                if token.user != user:
                    # If token exists but belongs to different user, update it
                    token.user = user
                    token.save()
            except Token.DoesNotExist:
                # If token doesn't exist with this key, delete any existing tokens for user
                Token.objects.filter(user=user).delete()
                # Create new token
                Token.objects.create(user=user, key=env_token)
            
            self.stdout.write(self.style.SUCCESS('Successfully initialized API token'))
