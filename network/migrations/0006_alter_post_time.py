# Generated by Django 3.2.4 on 2021-09-02 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_follower'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='time',
            field=models.CharField(max_length=19),
        ),
    ]