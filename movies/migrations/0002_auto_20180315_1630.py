# Generated by Django 2.0.1 on 2018-03-15 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='star',
            field=models.CharField(max_length=400),
        ),
        migrations.AlterField(
            model_name='movie',
            name='writer',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
