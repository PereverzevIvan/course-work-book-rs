# Generated by Django 4.2.2 on 2023-06-20 06:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Author",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("firstname", models.CharField(max_length=200)),
                ("lastname", models.CharField(max_length=200)),
                ("patronymic", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("book_name", models.CharField(max_length=200)),
                ("image_src", models.TextField()),
                ("year", models.IntegerField()),
                ("rating", models.IntegerField()),
                ("annotation", models.TextField()),
                ("bibliographic_record", models.TextField()),
                (
                    "author_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="RecommendSystem.author",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Genre",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("genre_name", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="Favorites",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "book_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="RecommendSystem.book",
                    ),
                ),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField()),
                ("created_at", models.DateField(auto_now_add=True)),
                ("rating", models.IntegerField()),
                (
                    "author_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="RecommendSystem.author",
                    ),
                ),
                (
                    "book_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="RecommendSystem.book",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="book",
            name="genre",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="RecommendSystem.genre"
            ),
        ),
        migrations.CreateModel(
            name="BlackList",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "book_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="RecommendSystem.book",
                    ),
                ),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
