# Generated by Django 3.1.6 on 2021-04-18 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='hehe',
            fields=[
                ('did', models.AutoField(primary_key=True, serialize=False)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('uid', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
