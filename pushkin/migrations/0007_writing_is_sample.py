# Generated by Django 2.2.7 on 2021-03-15 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pushkin', '0006_auto_20210315_1805'),
    ]

    operations = [
        migrations.AddField(
            model_name='writing',
            name='is_sample',
            field=models.BooleanField(default=False),
        ),
    ]
