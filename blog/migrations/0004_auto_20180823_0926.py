# Generated by Django 2.1 on 2018-08-23 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20180823_0919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='Body',
            field=models.TextField(verbose_name='متن پست'),
        ),
    ]
