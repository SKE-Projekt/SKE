# Generated by Django 3.0.6 on 2020-05-13 20:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('SKE_COURSES', '0004_courseexercise'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExerciseSubmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('special_id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('submission_date', models.DateTimeField(auto_now_add=True)),
                ('code', models.TextField(editable=False, max_length=24576)),
                ('result', models.IntegerField(choices=[(0, 'NIE SPRAWDZONO'), (1, 'BŁĄD SPRAWDZANIA'), (2, 'BŁĄD WYKONANIA'), (3, 'BŁĘDNY WYNIK'), (4, 'POPRAWNY WYNIK')], default=0)),
                ('author', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('exercise', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='SKE_COURSES.CourseExercise')),
            ],
        ),
    ]
