# Generated by Django 3.1.7 on 2021-03-05 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0002_auto_20210304_2205'),
    ]

    operations = [
        migrations.CreateModel(
            name='NameSpecializaion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', models.CharField(blank=True, max_length=50, unique=True)),
            ],
            options={
                'verbose_name': 'City',
                'verbose_name_plural': 'Citys',
            },
        ),
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('title', models.CharField(max_length=250)),
                ('company', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraping.city')),
                ('specialization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraping.namespecializaion')),
            ],
        ),
    ]