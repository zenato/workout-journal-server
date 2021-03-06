# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-07 00:03
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('unit', models.CharField(default='Kg', max_length=10, verbose_name='Unit')),
                ('value', models.SmallIntegerField(blank=True, null=True, verbose_name='Value')),
                ('remark', models.TextField(blank=True, verbose_name='Etc.')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Event',
            },
        ),
        migrations.CreateModel(
            name='Performance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.SmallIntegerField(blank=True, null=True, verbose_name='Value')),
                ('set1', models.SmallIntegerField(blank=True, null=True, verbose_name='Set 1')),
                ('set2', models.SmallIntegerField(blank=True, null=True, verbose_name='Set 2')),
                ('set3', models.SmallIntegerField(blank=True, null=True, verbose_name='Set 3')),
                ('set4', models.SmallIntegerField(blank=True, null=True, verbose_name='Set 4')),
                ('set5', models.SmallIntegerField(blank=True, null=True, verbose_name='Set 5')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='journal.Event', verbose_name='Event')),
            ],
            options={
                'verbose_name': 'Performance',
                'verbose_name_plural': 'Performance',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('workout_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Workout date')),
                ('remark', models.CharField(blank=True, max_length=200, null=True, verbose_name='Remark')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Post',
            },
        ),
        migrations.AddField(
            model_name='performance',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='performances', to='journal.Post'),
        ),
    ]
