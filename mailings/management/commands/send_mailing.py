from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from mailings.models import Client, Mailing, Message


class Command(BaseCommand):
    """Создаёт группу 'Менеджеры' и назначает права просмотра всех сущностей."""

    help = "Создаёт группу Менеджеры с нужными правами"

    def handle(self, *args, **options):
        group, _ = Group.objects.get_or_create(name="Менеджеры")
        perms = []
        for model, codename in [
            (Client, "view_all_clients"),
            (Message, "view_all_messages"),
            (Mailing, "view_all_mailings"),
            (Mailing, "stop_mailings"),
        ]:
            ct = ContentType.objects.get_for_model(model)
            perm = Permission.objects.get(content_type=ct, codename=codename)
            perms.append(perm)

        group.permissions.set(perms)
        self.stdout.write(self.style.SUCCESS("Группа 'Менеджеры' обновлена"))
