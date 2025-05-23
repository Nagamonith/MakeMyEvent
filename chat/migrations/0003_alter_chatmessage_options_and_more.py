# Generated by Django 4.2.20 on 2025-05-13 12:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0002_alter_chatmessage_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chatmessage',
            options={},
        ),
        migrations.RemoveField(
            model_name='chatmessage',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='chatmessage',
            name='retailer',
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='receiver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to=settings.AUTH_USER_MODEL),
        ),
    ]
