# Generated by Django 4.2.2 on 2023-06-21 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("RecommendSystem", "0007_alter_book_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="book",
            name="bibliographic_record",
        ),
        migrations.AlterField(
            model_name="book",
            name="image",
            field=models.ImageField(
                default="static/images/default.png", upload_to="static/images/"
            ),
        ),
    ]
