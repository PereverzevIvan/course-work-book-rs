# Generated by Django 4.2.2 on 2023-06-21 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("RecommendSystem", "0004_rename_favorites_favorite"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="book",
            name="image_src",
        ),
        migrations.AddField(
            model_name="book",
            name="image",
            field=models.ImageField(
                default="./static/images/default.png", upload_to="./static/images/"
            ),
        ),
    ]
