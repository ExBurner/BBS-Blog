# Generated by Django 2.0.6 on 2018-07-12 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20180712_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建日期'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建日期'),
        ),
        migrations.AlterField(
            model_name='user',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建日期'),
        ),
    ]
