# Generated by Django 5.1.7 on 2025-03-31 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0002_chat_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='message',
            field=models.TextField(null=True),
        ),
    ]
