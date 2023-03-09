from django.conf import settings


TOKEN_TIMEOUT = getattr(settings, 'TOKEN_TIMEOUT', 3600)
