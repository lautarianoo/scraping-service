# Generated by Django 3.1.7 on 2021-03-07 09:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0006_auto_20210306_1125'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='NameSpecialization',
            new_name='NameProf',
        ),
        migrations.RenameField(
            model_name='vacancy',
            old_name='specialization',
            new_name='prof',
        ),
    ]
