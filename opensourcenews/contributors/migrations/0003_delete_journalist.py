# Generated by Django 4.2.16 on 2024-12-12 18:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0008_journalist_alter_article_created_by'),
        ('contributors', '0002_journalist_first_name_journalist_last_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Journalist',
        ),
    ]