# Generated by Django 3.2.7 on 2021-09-01 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20210901_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionset',
            name='description',
            field=models.TextField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='questionset',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
