# Generated by Django 4.2.7 on 2025-05-09 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_user_token"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={
                "permissions": [("set_is_active", "Может блокировать пользователя")],
                "verbose_name": "Пользователь",
                "verbose_name_plural": "Пользователи",
            },
        ),
        migrations.AlterField(
            model_name="user",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="Активность"),
        ),
    ]
