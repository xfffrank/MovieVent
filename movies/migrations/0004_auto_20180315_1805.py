# Generated by Django 2.0.1 on 2018-03-15 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_auto_20180315_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='alternate_name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
