# Generated by Django 5.0.4 on 2024-05-08 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_course_description_alter_project_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='published_date',
            field=models.DateField(),
        ),
    ]