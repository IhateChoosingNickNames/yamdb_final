# Generated by Django 2.2.16 on 2023-03-05 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='title',
            name='smth',
            field=models.CharField(default='111', max_length=128),
        ),
    ]
