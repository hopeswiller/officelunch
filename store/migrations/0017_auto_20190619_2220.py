# Generated by Django 2.2.2 on 2019-06-19 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_order_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='comments',
            field=models.TextField(default='no comments yet..', max_length=500),
        ),
    ]
