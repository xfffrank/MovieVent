# Generated by Django 2.0.1 on 2018-03-15 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_auto_20180315_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='language',
            field=models.CharField(max_length=100),
        ),
    ]
