# Generated by Django 4.2.4 on 2023-08-17 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='actual_step',
            field=models.CharField(default='1', max_length=1, null=True),
        ),
    ]
