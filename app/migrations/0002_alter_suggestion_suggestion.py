# Generated by Django 5.1 on 2024-09-04 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suggestion',
            name='suggestion',
            field=models.CharField(max_length=1000),
        ),
    ]
