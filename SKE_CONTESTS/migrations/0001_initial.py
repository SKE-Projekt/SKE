# Generated by Django 3.0.6 on 2020-05-14 15:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('special_id', models.UUIDField(default=uuid.uuid4)),
                ('date_begin', models.DateTimeField()),
                ('date_end', models.DateTimeField()),
                ('body', models.TextField(max_length=24576)),
            ],
        ),
        migrations.CreateModel(
            name='ContestNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('body', models.TextField(max_length=24576)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SKE_CONTESTS.Contest')),
            ],
        ),
    ]
