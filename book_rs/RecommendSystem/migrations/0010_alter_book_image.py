# Generated by Django 4.2.2 on 2023-06-21 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("RecommendSystem", "0009_alter_book_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="image",
            field=models.ImageField(
                default="images/book_faces/default.png", upload_to="images/book_faces/"
            ),
        ),
    ]
