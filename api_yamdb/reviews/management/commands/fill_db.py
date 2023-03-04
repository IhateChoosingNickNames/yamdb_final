import csv
import os

from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title, User


class Command(BaseCommand):
    """Команда для наполнения БД из CSV-файлов."""

    help = "Filling DB with prepared CSV-files."
    data_folder = "static/data"
    schema = (
        (User, "users.csv"),
        (Genre, "genre.csv"),
        (Category, "category.csv"),
        (Title, "titles.csv"),
        (Title.genre.through, "genre_title.csv"),
        (Review, "review.csv"),
        (Comment, "comments.csv"),
    )

    def handle(self, *args, **options):
        for model, file in self.schema:
            with open(
                os.path.join(self.data_folder, file), encoding="UTF-8"
            ) as file:
                rows = csv.DictReader(file)
                result = [model(**row) for row in rows]
            model.objects.bulk_create(result)
