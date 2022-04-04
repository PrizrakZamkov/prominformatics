# Generated by Django 4.0.3 on 2022-04-04 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default='', max_length=255)),
                ('description', models.TextField(default='', max_length=2047)),
                ('path_link', models.TextField(max_length=255)),
                ('year', models.TextField(default='', max_length=255)),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('last_open_date', models.DateTimeField(auto_now_add=True)),
                ('author', models.TextField(max_length=255)),
                ('department', models.TextField(max_length=255)),
                ('mark', models.TextField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('src', models.TextField(max_length=255)),
                ('status', models.TextField(default='ordinary', max_length=255)),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.project')),
            ],
        ),
        migrations.CreateModel(
            name='DockerISO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link_to_iso', models.TextField(max_length=255)),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.project')),
            ],
        ),
    ]
