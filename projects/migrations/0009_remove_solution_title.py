# Generated by Django 2.1.8 on 2019-08-03 00:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_solution'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solution',
            name='title',
        ),
    ]
