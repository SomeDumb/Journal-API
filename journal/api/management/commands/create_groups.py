import logging

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

AUTHOR_PERMISSIONS = ['view', 'add', 'change', 'delete']
SUBSCRIBER_PERMISSIONS = ['view']

class Command(BaseCommand):
    help = 'Creates read only default permission groups for users'

    def handle(self, *args, **options):
        new_group, created = Group.objects.get_or_create(name='author')
        
        for permission in AUTHOR_PERMISSIONS:
            name = 'Can {} {}'.format(permission, 'article')
            print("Creating {}, for {}".format(name, new_group.name))
            try:
                model_add_perm = Permission.objects.get(name=name)
            except Permission.DoesNotExist:
                logging.warning("Permission not found with name '{}'.".format(name))
                continue
            new_group.permissions.add(model_add_perm)

        new_group, created = Group.objects.get_or_create(name='subscriber')
        for permission in SUBSCRIBER_PERMISSIONS:
            name = 'Can {} {}'.format(permission, 'article')
            print("Creating {}, for {}".format(name, new_group.name))
            try:
                model_add_perm = Permission.objects.get(name=name)
            except Permission.DoesNotExist:
                logging.warning("Permission not found with name '{}'.".format(name))
                continue
            new_group.permissions.add(model_add_perm)

        print("\nCreated default group and permissions.")