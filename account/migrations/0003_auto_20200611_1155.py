# Generated by Django 3.0.7 on 2020-06-11 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20200611_1019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='career',
            name='name',
            field=models.CharField(default='', max_length=200),
        ),
    ]