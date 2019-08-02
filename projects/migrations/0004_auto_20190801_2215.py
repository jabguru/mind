# Generated by Django 2.1.8 on 2019-08-01 21:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_project_team'),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=225, null=True)),
                ('message', models.TextField()),
                ('post_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='is_submitted',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='issue',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issues', to='projects.Project'),
        ),
    ]