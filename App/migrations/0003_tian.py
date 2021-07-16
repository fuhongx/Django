# Generated by Django 3.1.6 on 2021-04-18 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_hehe'),
    ]

    operations = [
        migrations.CreateModel(
            name='tian',
            fields=[
                ('uid', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=30, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('sex', models.CharField(choices=[('male', '男'), ('female', '女')], max_length=32)),
                ('phone', models.CharField(blank=True, max_length=30, null=True)),
            ],
        ),
    ]
