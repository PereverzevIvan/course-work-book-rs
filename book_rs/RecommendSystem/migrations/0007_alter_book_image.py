# Generated by Django 4.2.2 on 2023-06-21 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("RecommendSystem", "0006_alter_book_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="image",
            field=models.ImageField(
                default="./RecommendSystem/app_static/images/default.png",
                upload_to="./RecommendSystem/app_static/images/",
            ),
        ),
    ]
