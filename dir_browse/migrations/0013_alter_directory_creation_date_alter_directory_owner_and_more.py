# Generated by Django 4.1.7 on 2023-05-21 19:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dir_browse', '0012_alter_directory_creation_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='directory',
            name='creation_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='creation date'),
        ),
        migrations.AlterField(
            model_name='directory',
            name='owner',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='file',
            name='creation_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='creation date'),
        ),
        migrations.AlterField(
            model_name='file',
            name='owner',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='filesection',
            name='owner',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='sectionstatus',
            name='creation_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='creation date'),
        ),
        migrations.AlterField(
            model_name='sectionstatus',
            name='owner',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='sectiontype',
            name='creation_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='creation date'),
        ),
        migrations.AlterField(
            model_name='sectiontype',
            name='owner',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='statusdata',
            name='creation_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='creation date'),
        ),
        migrations.AlterField(
            model_name='statusdata',
            name='owner',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]