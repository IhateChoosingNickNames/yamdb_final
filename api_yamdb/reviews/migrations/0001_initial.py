# Generated by Django 2.2.16 on 2022-12-06 20:02

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import reviews.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=256, verbose_name='Имя категории')),
                ('slug', models.SlugField(unique=True, verbose_name='Слаг для URL')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=256, verbose_name='Название жанра')),
                ('slug', models.SlugField(unique=True, verbose_name='Слаг для URL')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=256, verbose_name='Название произведения')),
                ('year', models.PositiveSmallIntegerField(validators=[reviews.utils.year_validator], verbose_name='Год публикации')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='title', to='reviews.Category', verbose_name='Категория')),
                ('genre', models.ManyToManyField(related_name='title', to='reviews.Genre', verbose_name='Жанр')),
            ],
            options={
                'verbose_name': 'Произведение',
                'verbose_name_plural': 'Произведения',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=500, verbose_name='Текст отзыва')),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('score', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, 'Допустимы значения от 1 до 10'), django.core.validators.MaxValueValidator(10, 'Допустимы значения от 1 до 10')], verbose_name='Оценка')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор отзыва')),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review', to='reviews.Title', verbose_name='Произведение')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500, verbose_name='Текст комментария')),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор комментария')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='reviews.Review', verbose_name='Отзыв')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('author', 'title'), name='unique_review'),
        ),
    ]
