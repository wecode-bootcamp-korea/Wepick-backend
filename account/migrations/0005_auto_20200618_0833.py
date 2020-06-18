# Generated by Django 3.0.7 on 2020-06-18 08:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20200618_0818'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skill',
            name='profile',
        ),
        migrations.AddField(
            model_name='profile',
            name='skill',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.Skill'),
        ),
    ]