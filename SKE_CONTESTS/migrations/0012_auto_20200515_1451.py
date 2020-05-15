# Generated by Django 3.0.6 on 2020-05-15 12:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SKE_CONTESTS', '0011_auto_20200515_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contesttasksubmissiontest',
            name='submit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ttests', to='SKE_CONTESTS.ContestTaskSubmission'),
        ),
        migrations.AlterField(
            model_name='contesttasksubmissiontest',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SKE_CONTESTS.ContestTaskTest'),
        ),
    ]