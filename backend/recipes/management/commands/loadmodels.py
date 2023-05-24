import json

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("--path", type=str, help="file path")

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Старт команды'))

        with open('ingredients.json', encoding='utf-8',
                  ) as data_file_ingredients:
            ingredient_data = json.loads(data_file_ingredients.read())
            for ingredients in ingredient_data:
                Ingredient.objects.get_or_create(**ingredients)
        self.stdout.write(self.style.SUCCESS('Данные загружены'))
