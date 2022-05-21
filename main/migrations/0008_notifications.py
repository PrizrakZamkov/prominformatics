# Generated by Django 4.0.4 on 2022-05-21 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_project_student_uploader'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(default='', max_length=700)),
                ('send_time', models.DateTimeField(auto_now_add=True)),
                ('user_receiver', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='user_receiver', to='main.student')),
                ('user_sender', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='user_sender', to='main.student')),
            ],
        ),
    ]
