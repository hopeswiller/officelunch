# Generated by Django 2.2.2 on 2019-06-17 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_remove_employs_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='employs',
            name='password',
            field=models.CharField(default='asdf', max_length=50),
        ),
    ]