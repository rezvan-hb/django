# Generated by Django 2.2.3 on 2019-08-23 10:59

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users1', '0004_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Verify_email',
            fields=[
                ('email_verified', models.BooleanField()),
                ('verify_token', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
        ),
    ]