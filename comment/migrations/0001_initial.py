# Generated by Django 4.1.7 on 2023-03-29 06:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
        ('articles', '0002_news_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=50)),
                ('body', models.TextField()),
                ('articles', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.news')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.newscategory')),
            ],
        ),
    ]
