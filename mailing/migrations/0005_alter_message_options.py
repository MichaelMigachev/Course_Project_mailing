# Generated by Django 4.2.7 on 2025-05-13 06:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("mailing", "0004_alter_mailing_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="message",
            options={
                "ordering": ["topic"],
                "permissions": [("view_all_messages", "Может видеть все сообщения")],
                "verbose_name": "письмо",
                "verbose_name_plural": "письма",
            },
        ),
    ]
