# Generated by Django 5.1.7 on 2025-03-24 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangotanach', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='book',
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='word',
            name='chapter',
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='word',
            name='line',
            field=models.IntegerField(db_index=True),
        ),
    ]
