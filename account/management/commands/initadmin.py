import logging

from django.core.management.base import BaseCommand, CommandError

from account.models import User

logger = logging.getLogger('views')


class Command(BaseCommand):
    """Creates Superuser"""
    help = 'Create admin if it does not exist'

    def handle(self, *args, **options):
        if not User.objects.exists():
            admin = User.objects.create_superuser(username='+79376568217', password='123')
            admin.is_active = True
            admin.is_admin = True
            admin.save()
            logger.debug('Congratulations, Admin Account is created!')
        else:
            logger.debug('Admin accounts can only be initialized if no Users exist')
