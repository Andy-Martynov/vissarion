# Generated by Django 2.2.7 on 2021-03-21 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pushkin', '0007_writing_is_sample'),
    ]

    operations = [
        migrations.AlterField(
            model_name='writing',
            name='genre',
            field=models.CharField(choices=[('1', 'Проза'), ('2', 'Поэзия'), ('3', 'Неизвестно')], default='3', max_length=1),
        ),
    ]
