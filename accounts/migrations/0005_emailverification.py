# Generated by Django 2.2 on 2021-12-13 08:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20211129_0356'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailVerification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('name', models.CharField(blank=True, max_length=30)),
                ('token_key', models.CharField(max_length=40, unique=True)),
                ('is_used', models.BooleanField(default=False)),
                ('expiry', models.DateTimeField(default=datetime.datetime(2021, 12, 13, 9, 29, 39, 100527))),
                ('purpose', models.PositiveSmallIntegerField(choices=[(0, 'Signup'), (1, 'Group'), (2, 'Pokerboard')], default=0)),
            ],
        ),
    ]