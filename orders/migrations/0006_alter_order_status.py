# Generated by Django 5.0.3 on 2024-07-10 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_orderitem_lineitem_total_delete_orderlineitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Processing', 'Processing'), ('Shipped', 'Shipped'), ('Completed', 'Completed'), ('Refunded', 'Refunded'), ('Cancelled', 'Cancelled')], default='Pending', max_length=20),
        ),
    ]
