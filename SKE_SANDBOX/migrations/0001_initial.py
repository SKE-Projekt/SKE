# Generated by Django 3.0.6 on 2020-05-12 20:23

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
            name='SandboxSubmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('special_id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('submission_date', models.DateTimeField(auto_now_add=True)),
                ('result', models.IntegerField(choices=[(0, 'NIE SPRAWDZONO'), (1, 'BŁĄD SPRAWDZANIA'), (2, 'BŁĄD WYKONANIA'), (3, 'POPRAWNIE WYKONANO')], default=0)),
                ('author', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
