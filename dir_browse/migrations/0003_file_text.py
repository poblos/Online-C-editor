# Generated by Django 4.1.7 on 2023-05-07 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dir_browse', '0002_file_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='text',
            field=models.CharField(default='siema', max_length=10000),
        ),
    ]