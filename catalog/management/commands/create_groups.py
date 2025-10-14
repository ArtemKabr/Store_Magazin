from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from catalog.models import Product

class Command(BaseCommand):
    help = "Создаёт группу Модератор продуктов с нужными правами."

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name="Модератор продуктов")
        unpublish_perm = Permission.objects.get(codename="can_unpublish_product")
        delete_perm = Permission.objects.get(codename="delete_product")
        group.permissions.set([unpublish_perm, delete_perm])
        group.save()
        self.stdout.write(self.style.SUCCESS("Группа 'Модератор продуктов' настроена."))
