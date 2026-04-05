from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Экспортирует остатки товаров в JSON-файл'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help='Имя выходного JSON-файла')

    def handle(self, *args, **options):
        file_path = options['file']
        try:
            self.stdout.write(f'Экспорт остатков товаров в {file_path}...')
            call_command('dumpdata', 'Products.Product', '--output', file_path, '--indent', 4)
            self.stdout.write(self.style.SUCCESS(f'Остатки товаров успешно экспортированы в {file_path}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при экспорте данных: {e}'))