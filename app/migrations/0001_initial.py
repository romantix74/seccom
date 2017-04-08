# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-21 09:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ovpn_servers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server_title', models.CharField(max_length=30)),
                ('server_address', models.TextField()),
            ],
            options={
                'verbose_name': 'сервер',
                'verbose_name_plural': 'серверы',
            },
        ),
    ]
