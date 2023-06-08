# Generated by Django 4.1.7 on 2023-05-09 23:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dir_browse', '0011_statusdata_sectiontype_sectionstatus_filesection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='directory',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='creation date'),
        ),
        migrations.AlterField(
            model_name='file',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='creation date'),
        ),
        migrations.AlterField(
            model_name='sectionstatus',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='creation date'),
        ),
        migrations.AlterField(
            model_name='sectiontype',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='creation date'),
        ),
        migrations.AlterField(
            model_name='statusdata',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='creation date'),
        ),
    ]