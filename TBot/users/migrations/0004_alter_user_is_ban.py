# Generated by Django 3.2.3 on 2021-06-17 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_u_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_ban',
            field=models.BooleanField(default=False),
        ),
    ]
