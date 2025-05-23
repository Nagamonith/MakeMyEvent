# Generated by Django 4.2.20 on 2025-05-13 11:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Retailer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='retailer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.URLField(max_length=500)),
                ('service_type', models.CharField(max_length=100)),
                ('company_name', models.CharField(max_length=200)),
                ('specialization', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('website_link', models.URLField(max_length=500)),
                ('available', models.BooleanField(default=True)),
                ('retailer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='serviceprovider.retailer')),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('requirements', models.TextField()),
                ('payment', models.DecimalField(decimal_places=2, max_digits=10)),
                ('number_of_entries', models.IntegerField(default=1)),
                ('posted_on', models.DateTimeField(auto_now_add=True)),
                ('location', models.CharField(default='Not Specified', max_length=100)),
                ('retailer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serviceprovider.retailer')),
            ],
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
                ('retailer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serviceprovider.retailer')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages_sent', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
