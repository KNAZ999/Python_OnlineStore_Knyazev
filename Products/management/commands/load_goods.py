from django.core.management.base import BaseCommand
from django.core.management import call_command
import os

class Command(BaseCommand):
    help = 'Загружает данные о товарах из JSON-файла'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help='Путь к JSON-файлу с данными')

    def handle(self, *args, **options):
        file_path = options['file']

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'Файл не найден: {file_path}'))
            return

        try:
            # Читаем файл с поддержкой кириллицы (cp1251 для Windows)
            with open(file_path, 'r', encoding='cp1251') as f:
                data = f.read()

            # Сохраняем временно в UTF-8
            temp_file = 'temp_data_utf8.json'
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(data)

            self.stdout.write(f'Загрузка данных из {file_path}...')
            call_command('loaddata', temp_file)
            self.stdout.write(self.style.SUCCESS(f'Данные успешно загружены из {file_path}'))

        except UnicodeDecodeError as e:
            self.stdout.write(self.style.ERROR(f'Ошибка декодирования: {e}. Попробуйте сохранить файл в UTF-8 или cp1251.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при загрузке данных: {e}'))