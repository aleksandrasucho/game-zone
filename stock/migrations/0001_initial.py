# Generated by Django 3.2.24 on 2024-02-27 22:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='format: required, max_length=100', max_length=100, unique=True, verbose_name='Category Name')),
                ('slug', models.SlugField(help_text='format: required, max_length=150', max_length=150, unique=True, verbose_name='Category Slug')),
                ('is_active', models.BooleanField(choices=[(True, 'Active'), (False, 'Inactive')], default=False, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='format: required, max_length=150', max_length=150, unique=True, verbose_name='Product Name')),
                ('slug', models.SlugField(help_text='format: required, max_length=150', max_length=150, unique=True, verbose_name='Product Slug')),
                ('description', models.TextField(help_text='format: required', verbose_name='Product Description')),
                ('price', models.DecimalField(decimal_places=2, help_text='format: required', max_digits=10, verbose_name='Price')),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='Product Image')),
                ('category', models.ForeignKey(help_text='format: required', on_delete=django.db.models.deletion.CASCADE, related_name='products', to='stock.category', verbose_name='Category')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ProductInventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_available', models.PositiveIntegerField(default=0)),
                ('product', models.OneToOneField(help_text='format: required', on_delete=django.db.models.deletion.CASCADE, related_name='inventory', to='stock.product', verbose_name='Product')),
            ],
        ),
    ]
