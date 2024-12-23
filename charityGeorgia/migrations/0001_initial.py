# Generated by Django 5.1.4 on 2024-12-22 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Charity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('scraped_text', models.TextField()),
                ('website', models.URLField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='charity_images/')),
            ],
        ),
    ]