# Generated by Django 4.2.7 on 2025-05-16 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mailing", "0005_alter_message_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="client",
            options={
                "ordering": ["full_name"],
                "permissions": [("can_blocking_client", "Может блокировать получателя")],
                "verbose_name": "получатель",
                "verbose_name_plural": "получатели",
            },
        ),
        migrations.AddField(
            model_name="client",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="активность"),
        ),
    ]
