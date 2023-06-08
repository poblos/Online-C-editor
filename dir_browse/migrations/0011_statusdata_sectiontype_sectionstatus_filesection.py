# Generated by Django 4.1.7 on 2023-05-09 23:57

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dir_browse', '0010_dependantoption'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatusData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='New directory', max_length=200)),
                ('desc', models.CharField(blank=True, max_length=200)),
                ('creation_date', models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='creation date')),
                ('alive', models.BooleanField(default=True)),
                ('delete_date', models.DateTimeField(blank=True, null=True, verbose_name='delete date')),
                ('change_date', models.DateTimeField(blank=True, null=True, verbose_name='change date')),
                ('warning_line', models.IntegerField()),
                ('owner', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='dir_browse.user')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SectionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='New directory', max_length=200)),
                ('desc', models.CharField(blank=True, max_length=200)),
                ('creation_date', models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='creation date')),
                ('alive', models.BooleanField(default=True)),
                ('delete_date', models.DateTimeField(blank=True, null=True, verbose_name='delete date')),
                ('change_date', models.DateTimeField(blank=True, null=True, verbose_name='change date')),
                ('type', models.IntegerField(choices=[(1, 'PROCEDURE'), (2, 'COMMENT'), (3, 'DIRECTIVE'), (4, 'DECLARATION'), (5, 'ASSEMBLY')])),
                ('owner', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='dir_browse.user')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SectionStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='New directory', max_length=200)),
                ('desc', models.CharField(blank=True, max_length=200)),
                ('creation_date', models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='creation date')),
                ('alive', models.BooleanField(default=True)),
                ('delete_date', models.DateTimeField(blank=True, null=True, verbose_name='delete date')),
                ('change_date', models.DateTimeField(blank=True, null=True, verbose_name='change date')),
                ('type', models.IntegerField(choices=[(1, 'COMPILING'), (2, 'NOT_COMPILING'), (3, 'WARNINGS')])),
                ('data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dir_browse.statusdata')),
                ('owner', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='dir_browse.user')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FileSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alive', models.BooleanField(default=True)),
                ('delete_date', models.DateTimeField(blank=True, null=True, verbose_name='delete date')),
                ('change_date', models.DateTimeField(blank=True, null=True, verbose_name='change date')),
                ('name', models.CharField(max_length=200)),
                ('desc', models.CharField(max_length=200)),
                ('creation_date', models.DateTimeField(verbose_name='creation date')),
                ('start', models.IntegerField()),
                ('end', models.IntegerField()),
                ('owner', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='dir_browse.user')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dir_browse.file')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dir_browse.sectionstatus')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dir_browse.sectiontype')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
