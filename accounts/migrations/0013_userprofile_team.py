# Generated by Django 2.1.8 on 2019-08-02 19:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_team_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='team',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Team'),
        ),
    ]
