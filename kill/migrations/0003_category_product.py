# Generated by Django 4.1.3 on 2022-11-30 18:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kill', '0002_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('images', models.ImageField(null=True, upload_to='product_images')),
                ('price', models.FloatField(default=0.0, null=True)),
                ('quantity', models.IntegerField(null=True)),
                ('description', models.TextField(null=True)),
                ('category.json', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kill.category.json')),
            ],
        ),
    ]